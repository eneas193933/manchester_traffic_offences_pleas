from dateutil import parser
from django import template
from django.utils import formats

register = template.Library()


@register.filter(name='parse_date')
def parse_date(value):
    if isinstance(value, basestring):
        dt = parser.parse(value)
    else:
        dt = value
    return dt