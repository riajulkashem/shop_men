from datetime import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist


from utilities.variables import ADMIN

register = template.Library()


@register.filter
def is_admin(request): return request.user.role.name == ADMIN


@register.filter
def first_letters_of_word(name):
    return ''.join(''.join([''.join(s[0]) for s in name.split(' ')]).split('-')).upper()


@register.filter
def replace_space_into_(text):
    return str(text).replace(' ', '_')


@register.filter
def marks_list(student, queryset):
    return queryset.filter(student=student)


@register.filter
def get_hr_name(hr_list, index):
    return hr_list[index-1].name


@register.filter
def get_hr_id(hr_list, index):
    return hr_list[index-1].id


@register.filter
def is_absent(queryset, date):
    date = datetime.strptime(date, "%Y-%m-%d").date()
    try:
        if not queryset.get(date=date).is_absent:
            return 'checked'
    except ObjectDoesNotExist:
        pass
    return None
