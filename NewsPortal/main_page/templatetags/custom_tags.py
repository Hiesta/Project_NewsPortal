from django import template
from pprint import pprint

register = template.Library()


@register.simple_tag(takes_context=True)
def current_url(context, **kwargs):
    content = context['request'].GET.copy()

    for key, value in kwargs.items():
        content[key] = value
    return content.urlencode()


