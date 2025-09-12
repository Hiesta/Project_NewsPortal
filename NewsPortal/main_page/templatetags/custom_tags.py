from django import template
from pprint import pprint
from ..models import UserSubs

register = template.Library()


@register.simple_tag(takes_context=True)
def current_url(context, **kwargs):
    content = context['request'].GET.copy()

    for key, value in kwargs.items():
        content[key] = value
    return content.urlencode()


@register.simple_tag(takes_context=True)
def is_subscribed(context, category):
    user = context['request'].user
    if user.is_authenticated:
        return UserSubs.objects.filter(user=user, category=category).exists()
    return False
