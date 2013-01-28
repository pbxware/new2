# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('store.search.views',
    url(r'^$', 'search', name="index"),
    url(r'^/search_products', 'search_ajax_products', name="search_products"),
    url(r'^/search_pages', 'search_ajax_pages', name="search_pages"),
)
