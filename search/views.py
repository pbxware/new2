# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.db.models import Q
from cms.models.pagemodel import Page
from catalog.models import Category, Brand, Product
from haystack.query import SearchQuerySet


def search_page(query):
    pages = SearchQuerySet().filter(content=query).models(Page)
    return Paginator(pages, settings.SEARCH_RESULTS_PER_PAGE)


def search_products(category, brand, query):
    sqs = Product.objects.published(Q(name__icontains=query) | Q(full_name__icontains=query) | Q(short_description__icontains=query))

    if brand:
        sqs = sqs.filter(brands=brand)

    if category:
        cats = category.get_active_children()
        sqs = sqs.filter(category__in=cats)

    return Paginator(sqs, settings.SEARCH_RESULTS_PER_PAGE)


def search(request):
    if request.method == 'GET' and request.GET:
        brand = request.GET.get('brand', None)
        category = request.GET.get('category', None)
        query = request.GET.get('q', None)

        if brand:
            try:
                brand = Brand.objects.get(pk=brand)
            except Brand.DoesNotExists:
                brand = None

        if category:
            try:
                category = Category.objects.get(pk=category)
            except Category.DoesNotExists:
                category = None

        paginator_products = search_products(category, brand, query)
        try:
            products = paginator_products.page(1)
        except EmptyPage:
            products = paginator_products.page(paginator_products.num_pages)

        paginator_pages = search_page(query)
        try:
            pages = paginator_pages.page(1)
        except EmptyPage:
            pages = paginator_pages.page(paginator_pages.num_pages)
    else:
        raise Http404

    return render(request, 'search/search.html', {
        'products': products,
        'category': category,
        'curbrand': brand,
        'query': query,
        'query_url': request.META.get('QUERY_STRING', ''),
        'pages': pages
    })


def search_ajax_products(request):
    if not request.is_ajax():
        raise Http404
    if request.method == 'GET' and request.GET:
        brand = request.GET.get('brand', None)
        category = request.GET.get('category', None)
        query = request.GET.get('q', None)
        page = request.GET.get('page', 1)

        if brand:
            try:
                brand = Brand.objects.get(pk=brand)
            except Brand.DoesNotExists:
                brand = None

        if category:
            try:
                category = Category.objects.get(pk=category)
            except Category.DoesNotExists:
                category = None

        paginator_products = search_products(category, brand, query)
        try:
            products = paginator_products.page(page)
        except PageNotAnInteger:
            products = paginator_products.page(1)
        except EmptyPage:
            products = paginator_products.page(paginator_products.num_pages)
    else:
        raise Http404

    return render(request, 'search/search_ajax_products.html', {
        'products': products,
    })


def search_ajax_pages(request):
    if not request.is_ajax():
        raise Http404
    if request.method == 'GET' and request.GET:
        query = request.GET.get('q', None)
        page = request.GET.get('page', 1)

        paginator_pages = search_page(query)
        try:
            pages = paginator_pages.page(page)
        except PageNotAnInteger:
            pages = paginator_pages.page(1)
        except EmptyPage:
            pages = paginator_pages.page(paginator_pages.num_pages)
    else:
        raise Http404

    return render(request, 'search/search_ajax_pages.html', {
        'pages': pages
    })
