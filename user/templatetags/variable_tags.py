from django import template

from utilities.variables import ADMIN, MASTER_ADMIN

register = template.Library()


@register.filter
def is_admin(request): return request.user.role.name == ADMIN


@register.filter
def is_master(request): return request.user.role.name == MASTER_ADMIN


@register.filter
def is_superuser(request): return request.user.is_superuser
