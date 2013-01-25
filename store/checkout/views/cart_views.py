# coding=utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from currencies.models import Currency
from store.catalog.models import Product
from django.contrib import messages
from store.catalog.utils import convert_price
from django.conf import settings
from djantix.shortcuts import redirect_to_back
from checkout.models import ExtCart
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from delivery.CDEK import delivery_to_location


def add_to_cart(request):
    if not (request.is_ajax() and request.method == 'POST'):
        raise Http404
    currency = None
    status = False
    mess = []
    try:
        quantity = int(request.POST.get('quantity', 1))
        product_id = int(request.POST.get('product_id', None))
    except ValueError:
        mess.append(_('Data entry errors'))
    except TypeError:
        mess.append(_('Data entry errors'))
    else:
        try:
            currency = Currency.objects.get(code__exact=settings.DEFAULT_CURRENCY)
        except Currency.DoesNotExist:
            currency = Currency.objects.all()
            if not currency:
                mess.append(_('Exchange rate error'))
            else:
                currency = currency[0]

        if currency:
            try:
                product = Product.objects.get(pk=product_id, is_active=True)
            except Product.DoesNotExist:
                mess.append(_('Product not found'))
            else:
                cart = ExtCart(request)
                cart.add(product, convert_price(product, currency), quantity)
                status = True
                if quantity > 1:
                    mess.append(_('%(name)s x%(count)s added to cart') % {'name': product.name, 'count': quantity})
                else:
                    mess.append(_('%s added to cart') % product.name)
    return HttpResponse(simplejson.dumps({
        'status': status,
        'messages': mess
    }), mimetype='application/javascript')


def update_cart(request):
    if not request.method == 'POST':
        raise Http404
    mess = []
    try:
        quantity = int(request.POST.get('quantity', 1))
        product_id = int(request.POST.get('product_id', None))
    except ValueError:
        mess.append(_('Data entry errors'))
    else:
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            messages.append(_('Product not found'))
        else:
            if quantity > 0:
                cart = ExtCart(request)
                cart.update(product, quantity)
                messages.info(request, _("Number of %(name)s updated by %(count)s") % {'name': product.name, 'count': quantity})
    return redirect_to_back(request)


def remove_from_cart(request, product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        raise Http404

    product = get_object_or_404(Product, pk=product_id)
    cart = ExtCart(request)
    cart.remove(product)
    messages.info(request, _("%s product is deleted from cart") % product)
    return redirect_to_back(request)


def show_cart(request):
    return render(request, 'cart/cart.html', {})


def cart_delivery(request):
    if not request.is_ajax():
        raise Http404
    price = 0
    result = None
    html = ''
    cart = ExtCart(request)
    if request.method == 'POST':
        location = request.session.get('cdek_location', None)
        if location and cart.count():
            result = delivery_to_location(location.id, cart)
            if result:
                price = result.get('price', 0)
                location_name = ', '.join(
                    [name for name in (location.city, location.region) if name]
                )
                html = loader.render_to_string('cart/cart_delivery.html', {
                    'location_name': location_name,
                    'delivery': result
                }, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({
        'summary': str(cart.summary()),
        'price': str(price),
        'html': html
    }), mimetype='application/javascript')
