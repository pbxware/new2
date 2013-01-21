# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('store.catalog.views.catalog',
    url(r'^tools/navigator$', 'navigator', name='navigator'),
    url(r'^product/(?P<slug_pro>[0-9A-Za-z-_//]+)$', 'show_product', name='show_product'),
    url(r'^$', 'index', name='index'),
    url(r'^(?P<slug>[0-9A-Za-z-_//]+)$', 'category', name='category'),
)
