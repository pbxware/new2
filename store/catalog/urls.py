# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('store.catalog.views.catalog',
    url(r'^tools/navigator$', 'navigator', name='navigator'),

    url(r'^$', 'index', name='index'),
    url(r'^(?P<slug>[0-9A-Za-z-_//]+)$', 'category', name='category'),
)
