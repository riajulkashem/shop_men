import re
from collections import OrderedDict
from json import loads, dumps

from django.contrib.auth.models import Group, Permission
from django.core.cache import cache
from django.urls import path
from rest_framework import status

from utilities.variables import SUPER_ADMIN


def is_valid_phone_number(phone: str):
    if re.match(r'^(?:\+8801|01)?(?:\d{9}|\d{8})$', phone):
        return True
    return False


def camel_case_split_underscore(string: str):
    return '_'.join(
        re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', string)
    ).lower()


def underscore_convert_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def permitted(request, permission_type, obj, self=None):
    if request.user.is_active and request.user.is_superuser:
        return True

    permission = '{0}.{1}_{2}'.format(
        str(obj._meta.app_label), permission_type,
        str(obj._meta.model_name)
    )
    if request.user.has_perm(permission):
        return True
    if self:
        self.message = "You have no {0} permission for {1}" \
            .format(permission_type, obj._meta.verbose_name)
    return False


def check_permitted(request, obj, self):
    if request.method == "GET" and not permitted(request, 'view', obj, self):
        return False
    if request.method == "POST" and not permitted(request, 'add', obj, self):
        return False

    if request.method in ["PUT", "PATCH"] and not permitted(request, 'change',
                                                            obj, self):
        return False

    if request.method == "DELETE" and not permitted(
            request,
            'delete',
            obj,
            self
    ):
        return False
    return True


def create_group_permission(group_permissions: dict):
    for group_name in group_permissions:

        # Get or create group
        group, created = Group.objects.get_or_create(name=group_name)

        # Loop models in group
        for model_cls in group_permissions[group_name]:
            # Loop permissions in group/model
            for perm_index, perm_name in \
                    enumerate(group_permissions[group_name][model_cls]):

                # Generate permission name as Django would generate it
                codename = perm_name + "_" + model_cls._meta.model_name

                try:
                    # Find permission object and add to group
                    perm = Permission.objects.get(codename=codename)
                    group.permissions.add(perm)
                    # print("Adding " + codename
                    #       + " to group "
                    #       + group.__str__())
                except Permission.DoesNotExist:
                    pass
                # print(codename + " not found")


def assign_user(user):
    if user.role.name != SUPER_ADMIN:
        filtered_group = Group.objects.filter(name=user.role.name)
        if not filtered_group.exists() or \
                not filtered_group[0].permissions.exists():
            # if user.role.name == ADMIN:
            #     create_group_permission(ADMIN_GROUP_PERMISSIONS)
            # elif user.role.name == MASTER_ADMIN:
            #     create_group_permission(MASTER_GROUP_PERMISSIONS)
            # TODO: Implement Permission assign
            #  func for ACCOUNTANT, STUDENT, Teacher
            permission_group = Group.objects.get(name=user.role.name)
            permission_group.user_set.add(user)
        else:
            permission_group = Group.objects.get(name=user.role.name)
            permission_group.user_set.add(user)

    return None


def process_data(request, model):
    data = request.data
    ids = [data[i].pop('id') for i in range(len(data))]
    object_list = model.objects.filter(id__in=ids)
    batch_size = len(object_list)
    if len(data) == batch_size:
        ln = length = len(data)
        fields = []
        for hr in object_list:
            dict_item = data[length - ln]
            for i in range(len(dict_item)):
                setattr(hr, list(dict_item.keys())[i],
                        dict_item[list(dict_item.keys())[i]])
                fields.append(list(dict_item.keys())[i])
            ln -= 1
        model.objects.bulk_update(object_list, fields=fields,
                                  batch_size=batch_size)
        return [status.HTTP_200_OK,
                {'success': 'All Info Updated Successfully'}]
    return [status.HTTP_400_BAD_REQUEST, {'error': 'Invalid Data Format'}]


def print_test_response(input_ordered_dict: OrderedDict) -> None:
    print(dumps(loads(dumps(input_ordered_dict)), indent=4))


def get_urls_for_views(views):
    url_patterns = []
    for v in dir(views):
        if 'CRUD' in v:
            url_name = v.split('CRUDView')[0].lower()
            view = getattr(getattr(views, v), 'as_view')()
            url_patterns += [
                path(url_name + '/', view, name=url_name),
                path(url_name + '/status/<int:pk>/', view,
                     name=url_name + '_status'),
                path(url_name + '/update/<int:pk>/', view,
                     name=url_name + '_update'),
                path(url_name + '/delete/<int:pk>/', view,
                     name=url_name + '_delete'),
            ]
    return url_patterns


def get_queryset_from_cache(model):
    queryset = cache.get('%s-queryset' % model._meta.model_name)
    if queryset:
        print('queryset returning from cache')
        return queryset
    queryset = model.objects.all()
    cache.set('%s-queryset' % model._meta.model_name, queryset, 600)
    print('queryset returning from DB')
    return queryset


def get_request_redirect(request, url):
    return url + '?' + str(request.get_raw_uri()).split('?')[1]
