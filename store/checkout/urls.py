# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('store.checkout.views.cart_views',
    url(r'^cart$', 'show_cart', name="show_cart"),
    url(r'^cart/add', 'add_to_cart', name="add_to_cart"),
    url(r'^cart/update', 'update_cart', name="update_cart"),
    url(r'^cart/remove/(?P<product_id>\d+)', 'remove_from_cart', name="remove_from_cart"),
    url(r'^cart/delivery$', 'cart_delivery', name="cart_delivery"),
)

urlpatterns += patterns('store.checkout.views.order_views',
    url(r'^order/create', 'create_order', name='create_order'),
    url(r'^order/(?P<order_id>\d+)', 'show_order', name='show_order'),
    url(r'^order/history$', 'show_order_list_history', name='show_order_list_history'),
    url(r'^order$', 'show_order_list', name='show_order_list'),
)

urlpatterns += patterns('store.checkout.views.report_views',
    url(r'^report/invoice/(?P<order_id>\d+)', 'invoice', name='invoice_report'),
)
