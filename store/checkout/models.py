# coding=utf-8
from cart import Cart, models as cart_models
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from catalog.models import Product
from datetime import datetime
from decimal import Decimal, ROUND_UP
from currencies.models import Currency


ACTIVE_STATUS = (
        ('new', _('New')),
        ('open', _('Opened')),
        ('paid', _('Paid')),
        ('sent', _('Sent')),
    )

NOT_ACTIVE_STATUS = (
        ('close', _('Closed')),
        ('cancel', _('Canceled'))
)

CHOICE_STATUS = ACTIVE_STATUS + NOT_ACTIVE_STATUS


class OrderManager(models.Manager):
    def active(self, *args, **kwargs):
        act_status = [status for status, value in ACTIVE_STATUS]
        return self.filter(status__in=act_status, *args, **kwargs)

    def not_active(self, *args, **kwargs):
        act_status = [status for status, value in NOT_ACTIVE_STATUS]
        return self.filter(status__in=act_status, *args, **kwargs)

    def neworders(self, *args, **kwargs):
        return self.filter(status='new', *args, **kwargs)


class ExtCart(Cart):
    def update(self, product, quantity, unit_price=None):
        try:
            item = cart_models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            pass
        else:
            item.quantity = quantity
            item.save()


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default='new')
    owner = models.ForeignKey(User, related_name='manager_orders')
    manager = models.ForeignKey(User, blank=True, null=True)

    date_added = models.DateTimeField(_("Date added"), editable=False)
    date_updated = models.DateTimeField(_("Date updated"), editable=False)
    date_closed = models.DateTimeField(_("Date closed"), editable=False, blank=True, null=True)

    objects = OrderManager()

    def save(self, *args, **kwargs):
        if not self.date_added:
            self.date_added = datetime.now()
        self.date_updated = datetime.now()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s: %s" % (self.owner,
            ', '.join([product.name for product in self.products.all()]))

    def summary(self, currency=None):
        if not currency:
            try:
                currency = Currency.objects.get(code__exact=settings.DEFAULT_CURRENCY)
            except Currency.DoesNotExist:
                currency = Currency.objects.all()
                if currency:
                    currency = currency[0]
        result = Decimal(0)
        for item in self.items.all():
            result += item.total_price(currency)
        return result

    def total_price(self, currency=None):
        return self.summary(currency) + self.delivery_price()

    def delivery_price(self):
        return self.delivery_cdek.price

    def get_items(self):
        return self.items.all()

    def is_owner(self, user):
        return self.owner == user


class OrderProduct(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order, related_name='items')
    quantity = models.PositiveIntegerField()

    current_price = models.DecimalField(_("Current price"), max_digits=14, decimal_places=6)
    currency = models.ForeignKey(Currency)
    discount = models.PositiveIntegerField(_('Discount'), default=0, blank=True)

    def total_price(self, currency=None):
        discount = self.discount or 0
        discount = Decimal((100 - discount) / 100.0).quantize(Decimal('.01'), rounding=ROUND_UP)
        return self.unit_price(currency) * self.quantity * discount

    def unit_price(self, currency=None):
        price = self.current_price
        if currency and self.currency != currency:
            price *= currency.factor
        return price


class TrackOrder(models.Model):
    order = models.ForeignKey(Order, related_name='tracking')
    status = models.CharField(max_length=10, choices=CHOICE_STATUS)
    date_added = models.DateTimeField(_("Date added"), editable=False, default=datetime.now)
    performer = models.ForeignKey(User)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('TrackOrder')
        verbose_name_plural = _('TrackOrders')

    def __unicode__(self):
        return "%s: %s" % (self.order.id, self.status)
