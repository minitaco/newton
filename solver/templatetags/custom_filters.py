from django import template

register = template.Library()


@register.filter
def ordinal(value):
    """
    Converts an integer to its ordinal as a string.
    1 -> '1st', 2 -> '2nd', 3 -> '3rd', etc.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    suffixes = ['th', 'st', 'nd', 'rd', 'th'][min(value % 10, 4)]
    if 11 <= (value % 100) <= 13:
        suffixes = 'th'
    return "%d%s" % (value, suffixes)