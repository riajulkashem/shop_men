from django import template

register = template.Library()


@register.filter
def has_msg(user):
    if user.staff_shop:
        msg = user.staff_shop.msg_list.filter(
            is_active=True
        )
        if msg.exists():
            return msg[0].msg
    return ''
