# coding=utf-8
from datetime import datetime
from django.conf import settings
from djantix.shortcuts import get_or_none
from checkout.models import ExtCart, Order, OrderProduct, TrackOrder
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from delivery.CDEK import delivery_to_location
from delivery.CDEK.models import Delivery, Tariff
from currencies.models import Currency
from django.utils.translation import ugettext_lazy as _
from account.models import Contact


@login_required
def create_order(request):
    result = None
    cart = ExtCart(request)
    location = request.session.get('cdek_location', None)
    if not cart.count():
        return redirect('checkout:show_cart')
    order = Order.objects.create(
        status='new',
        owner=request.user,
        date_added=datetime.now(),
    )
    try:
        currency = Currency.objects.get(code__exact=settings.DEFAULT_CURRENCY)
    except Currency.DoesNotExist:
        currency = Currency.objects.all()
        if currency:
            currency = currency[0]
    for cart_item in cart:
        OrderProduct.objects.create(
            order = order,
            quantity = cart_item.quantity,
            product = cart_item.get_product(),
            current_price = cart_item.unit_price,
            currency = currency
        )
    TrackOrder.objects.create(
        order = order,
        status = 'new',
        description = _('Order create'),
        date_added = datetime.now(),
        performer = request.user
    )
    if location:
        try:
            currency = Currency.objects.get(code__exact=settings.DELIVERY_CURRENCY)
        except Currency.DoesNotExist:
            currency = Currency.objects.all()
            if currency:
                currency = currency[0]
        args = {
            'order': order,
            'location_to': '%s, %s' % (location.city, location.region),
            'location_to_id': location.id,
            'date_added': datetime.now(),
            'currency': currency
        }
        result = delivery_to_location(location.id, cart)
        if result:
            args['tariff'] = get_or_none(Tariff, cdek_id=result['tariffId'])
            args['price'] = result.get('price', 0)
            args['min_days'] = result.get('deliveryPeriodMin', None)
            args['max_days'] = result.get('deliveryPeriodMax', None)
            Delivery.objects.create(**args)
    cart.clear()
    return redirect('checkout:show_order', order.id)


@login_required
def show_order_list(request):
    contact, create = Contact.objects.get_or_create(user=request.user)
    orders = Order.objects.active(owner=request.user)
    return render(request, 'checkout/order_list.html', {
        'orders': orders,
        'contact': contact,
    })


@login_required
def show_order_list_history(request):
    contact, create = Contact.objects.get_or_create(user=request.user)
    orders = Order.objects.not_active(owner=request.user)
    return render(request, 'checkout/order_list.html', {
        'orders': orders,
        'contact': contact,
    })


@login_required
def show_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    contact, create = Contact.objects.get_or_create(user=request.user)
    if not order.is_owner(request.user):
        return redirect('checkout:show_order_list')
    return render(request, 'checkout/order.html', {
        'order': order,
        'contact': contact,
    })
