from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    return int(value) / int(arg) if int(arg) != 0 else 0