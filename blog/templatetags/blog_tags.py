from django import template
from django.utils.html import mark_safe
import markdown

register = template.Library()

@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter
def markdownify(text):
    return mark_safe(markdown.markdown(text, extensions=['extra', 'nl2br', 'fenced_code', 'codehilite'], extension_configs={'codehilite': {'css_class': 'highlight', 'noclasses': True}}))
