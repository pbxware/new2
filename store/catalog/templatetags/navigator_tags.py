# coding=utf-8
from django import template
from store.catalog.models import Category

register = template.Library()

@register.inclusion_tag('store/catalog/navigator_item.jade', takes_context=True)
def show_navigator_item(context, item):
    if not isinstance(item, Category):
        raise template.TemplateSyntaxError, 'Given argument must be a MenuItem object.'
    context['item'] = item
    return context
