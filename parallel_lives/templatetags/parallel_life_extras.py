from django import template

register = template.Library()


@register.filter
def stars(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return ""
    return "★" * max(0, value)