# coding=utf-8
from django.shortcuts import get_object_or_404, render
from store.catalog.models import Category


def index(request):
    return render(request, 'store/index.jade', {

    })


def category(request, slug):
    category = get_object_or_404(Category, external_slug=slug, is_active=True)
    if category.has_active_children():
        return render(request, 'store/catalog/category.jade', {
            'category': category,
        })
    else:
        return render(request, 'store/catalog/category_list.jade', {
            'category': category,
        })


def navigator(request):
    pass
