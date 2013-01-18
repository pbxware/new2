# coding=utf-8
from django import template
from store.catalog.models import Category

register = template.Library()


@register.inclusion_tag('store/catalog/menu/catalog_menu.jade', takes_context=True)
def show_catalog_menu(context, category=None):
    root_categories = Category.objects.active(parent=None)
    categories = []
    if category:
        categories = category.parents()
        categories.append(category)
    return {
        'path': context['request'].path,
        'root_categories': root_categories,
        'categories': categories
    }


@register.inclusion_tag('store/catalog/menu/catalog_menu_item.jade', takes_context=True)
def show_menu_item(context, menu_item):
    if not isinstance(menu_item, Category):
        raise template.TemplateSyntaxError, 'Given argument must be a MenuItem object.'
    context['menu_item'] = menu_item
    return context
