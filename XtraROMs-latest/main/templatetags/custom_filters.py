from django import template
from main.models import *

register = template.Library()

@register.filter(name='get_key')
def get_key(dictionary, key):
    return dictionary.get(key, None)