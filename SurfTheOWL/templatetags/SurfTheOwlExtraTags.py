from django import template

register = template.Library()


def value_is_list(value):
    if isinstance(value, list):
        return True
    else:
        return False
register.filter('value_is_list', value_is_list)