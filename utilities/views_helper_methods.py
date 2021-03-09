import operator
from functools import reduce

from django.db.models import Q
from django.template.loader import render_to_string


def create_form(self, request):
    form = self.get_form()
    # Setup context data
    context = {
        'form': form,
        'form_title': 'Create New ' + self.model._meta.verbose_name
    }
    if self.submit:  # if true add submit button html snippets in context
        context['submit'] = \
            '<input type="submit" name="submit" ' \
            'value="Save" class="btn btn-primary float-right mb-2"' \
            ' id="submit-id-submit">'

    html_form = render_to_string(
        # render context with template as string form modal popup
        template_name='snippets/modal_form.html',
        context=context,
        request=request
    )
    return html_form


def update_form(self, request):
    form = self.get_form()
    obj = self.model._meta
    # Setup context data
    context = {
        'form': form,
        'form_title': 'Update ' + str(self.object),
        'form_url': '/' + obj.app_label + '/' +
                    obj.model_name + '/update/' + str(self.object.id) + '/'
    }
    if self.submit:  # if true add submit button html snippets in context
        context['submit'] = \
            '<input type="submit" name="submit" ' \
            'value="Save" class="btn btn-primary float-right mb-2"' \
            ' id="submit-id-submit">'
    if self.has_update_url:
        context['form_url'] = self.object.get_update_url()
    html_form = render_to_string(
        # render context with template as string form modal popup
        template_name='snippets/modal_form.html',
        context=context,
        request=request
    )
    return html_form


def search_query(self, value, queryset):
    searchable_fields = ['AutoField', 'CharField', 'EmailField',
                         'BigIntegerField', 'IntegerField']
    search = list()
    for field in self.model._meta.get_fields():
        if field.get_internal_type() in searchable_fields:
            search.append(Q(**{field.name + '__icontains': value}))
    return queryset.filter(reduce(operator.or_, search))
