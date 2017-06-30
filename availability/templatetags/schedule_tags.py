from django import template

register = template.Library()


@register.simple_tag
def timelabel(value):
    if value == 0:
        return 12
    elif value <= 12:
        return value
    else:
        return value % 12
