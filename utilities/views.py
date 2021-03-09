from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpRequest
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from utilities.methods import get_model_foreignkey_fields, \
    get_model_manytomany_fields, render_pdf
from utilities.views_helper_methods import create_form, update_form, \
    search_query


class CRUDView(
    SingleObjectTemplateResponseMixin,
    ModelFormMixin,
    ProcessFormView,
    AccessMixin
):
    """
    CRUD View provide create update delete functionality from on view
    """
    submit = True
    assign_shop = True
    has_update_url = False
    pdf_response = False
    pdf_template = None
    pdf_file_name = None
    paginated_by = 10
    queryset = None

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy(
            self.model._meta.app_label + ':' + self.model._meta.model_name
        )

    def get_cache_key(self):
        return '%s-queryset-%s' % (self.model._meta.model_name,
                                   self.request.user.id)

    def get_permission_denied_message(self):
        """
        Override this method to override
        the permission_denied_message attribute.
        """
        messages.error(self.request, self.permission_denied_message)
        return self.permission_denied_message

    def dispatch(self, request, *args, **kwargs):
        """
        :return: view after checking all required permission
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.is_permitted(request, 'view'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def has_shop(self):
        return self.request.user.staff_shop_id is not None

    def is_permitted(self, request: HttpRequest, permission_type: str):
        if request.user.is_active and request.user.is_superuser:
            return True

        permission = '{0}.{1}_{2}'.format(
            str(self.model._meta.app_label),
            permission_type,
            str(self.model._meta.model_name)
        )
        if request.user.has_perm(permission):
            return True
        self.permission_denied_message = \
            "You have no {0} permission..!".format(
                permission_type
            )
        return False

    def get_object(self, queryset=None):
        try:
            return super(CRUDView, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.pdf_response:
            if self.pdf_template is None or self.pdf_file_name is None:
                raise ValueError('PDF File Name And Template Name Must Be Set')
            return render_pdf(
                request=request,
                template=self.pdf_template,
                context=self.get_context_data(),
                file_name=self.pdf_file_name
            )
        if request.GET.get('page'):
            return super(CRUDView, self).get(request, *args, **kwargs)
        if request.is_ajax():

            if 'update' in request.path:
                if self.object and self.is_permitted(
                        request,
                        'change'
                ):  # if has permission to change object then render form

                    return JsonResponse(
                        data={'html_form': update_form(self, request)}
                    )

            if self.is_permitted(
                    request,
                    'add'
            ):  # if has permission to add object then render form

                return JsonResponse(
                    data={'html_form': create_form(self, request)}
                )

            return JsonResponse(
                data={'error': 'Error Permission Denied For You'})

        return super(CRUDView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'confirm_delete' in request.POST:
            if self.is_permitted(request, 'delete'):
                name = self.object
                try:
                    self.object.delete()
                    messages.success(
                        self.request, str(
                            self.model._meta.verbose_name
                        ).capitalize() + ' ' + str(
                            name) + ' Delete Successfully'
                    )
                    cache.delete(self.get_cache_key())
                    return JsonResponse({'msg': "Deleted Successfully"})
                except ProtectedError:
                    return JsonResponse(
                        {'error': "Can\'t Delete It has some depended data"}
                    )

            self.permission_denied_message = "You have no delete permission..!"
            return JsonResponse({'error': self.permission_denied_message})

        if self.object and self.is_permitted(
                request,
                'change'
        ) or self.is_permitted(
            request, 'add'
        ):
            return super(CRUDView, self).post(request, *args, **kwargs)
        self.permission_denied_message = \
            "You have no create or add permission..!"
        return self.handle_no_permission()

    def form_valid(self, form):
        cache.delete(self.get_cache_key())
        if self.object:
            form = self.get_form()
            messages.success(self.request,
                             f'{self.object} Update Successfully')
        else:
            form.instance.creator = self.request.user
            if self.assign_shop:
                form.instance.shop_id = self.request.user.staff_shop_id
            messages.success(
                self.request,
                f'{self.model._meta.verbose_name} Created Successfully'
            )

        return super().form_valid(form)

    def get_queryset(self):
        queryset = cache.get(self.get_cache_key())
        if queryset:
            return self.get_filtered_queryset(queryset)
        if self.queryset:
            queryset = self.queryset
        else:
            queryset = self.model.objects.select_related(
                *get_model_foreignkey_fields(self.model)
            ).prefetch_related(
                *get_model_manytomany_fields(self.model)
            ).all()
        cache.set(self.get_cache_key(), queryset, 600)
        return self.get_filtered_queryset(queryset.order_by('updated'))

    def paginated_list(self, object_list):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(object_list, self.paginated_by)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        return objects

    def get_filtered_queryset(self, queryset):
        filter_dict = {}
        search_value = None
        fields = []
        for field in queryset.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                fields.append(field.name + '_id')
            else:
                fields.append(field.name)

        for key, value in dict(self.request.GET).items():
            if key == 'search':
                search_value = self.request.GET.get(key)
                continue
            if key == 'page':
                continue
            if self.request.GET.get(key) != '' and key in fields:
                filter_dict[key] = self.request.GET.get(key)
        object_list = queryset.filter(**filter_dict)
        if search_value:
            object_list = search_query(self, search_value, object_list)
        if self.assign_shop:
            object_list = object_list.filter(shop=self.request.user.staff_shop)
        return object_list

    def get_paginated_list(self):
        object_list = self.get_queryset()
        return self.paginated_list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['app_label'] = self.model._meta.app_label
        context['object_list'] = self.get_paginated_list()
        context['total_found'] = self.get_queryset().count()
        context['permitted_for_delete'] = self.is_permitted(
            request=self.request, permission_type='delete')
        context['permitted_for_view'] = self.is_permitted(
            request=self.request,
            permission_type='view'
        )
        context['permitted_for_change'] = self.is_permitted(
            request=self.request,
            permission_type='change'
        ) and self.has_shop()
        context['permitted_for_add'] = self.is_permitted(
            request=self.request,
            permission_type='add'
        ) and self.has_shop()
        if self.submit:  # if true add submit button html snippets in context
            context['submit'] = \
                '<input type="submit" name="submit" ' \
                'value="Save" class="btn btn-primary float-right mb-2"' \
                ' id="submit-id-submit">'
        try:
            context['url_params'] = '?' + \
                                    self.request.get_full_path().split('?')[
                                        1] + '&page='
        except IndexError:
            context['url_params'] = '?page='
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
