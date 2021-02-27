import re
import tempfile
from collections import OrderedDict
from json import loads, dumps

from django.core.cache import cache
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path

from weasyprint import HTML


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


def render_pdf(request, template, context, file_name: str):
    html_string = render_to_string(
        template, context, request=request
    )
    html = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    )
    result = html.write_pdf()

    # Creating http response

    response = HttpResponse(content_type='application/pdf;')
    response[
        'Content-Disposition'] = 'inline; filename=' + file_name + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response


def get_model_fields(model):
    fields = []
    for field in model._meta.get_fields():
        if isinstance(field, models.ForeignKey):
            fields.append(field.name + '_id')
        else:
            fields.append(field.name)
    return fields


def get_model_foreignkey_fields(model):
    fields = []
    for field in model._meta.get_fields():
        if isinstance(field, models.ForeignKey):
            fields.append(field.name)
    return fields


def get_model_manytomany_fields(model):
    fields = []
    for field in model._meta.get_fields():
        if isinstance(field, models.ManyToManyField) \
                or isinstance(field, models.ManyToManyRel):
            fields.append(field.name)
    return fields
