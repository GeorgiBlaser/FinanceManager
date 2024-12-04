from django import template

register = template.Library()


@register.filter
def get(value, arg):
    """Извлича стойността за даден ключ от речник."""
    try:
        return value.get(arg)
    except AttributeError:
        return None
