import urllib
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def update_url_params(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return urllib.parse.urlencode(query)
