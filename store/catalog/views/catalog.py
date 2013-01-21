# coding=utf-8
from django.shortcuts import get_object_or_404, render
from store.catalog.models import Category, Product


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


def show_product(request, slug_pro):
    product = get_object_or_404(Product, slug=slug_pro, is_active=True)
    category = product.main_category
    return render(request, 'store/catalog/product.jade', {
        'product': product,
        'category': category,
    })
