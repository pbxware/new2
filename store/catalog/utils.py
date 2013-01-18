# coding=utf-8
from django.utils.encoding import smart_unicode
import re
import unicodedata
from htmlentitydefs import name2codepoint
from decimal import Decimal, ROUND_UP
from pytils import translit


def slugify(s, entities=True, decimal=True, hexadecimal=True,
    instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(translit.translify(unicode(s)))
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = re.sub(r'[^-a-z0-9_]+', '-', s.lower())
    return re.sub('-{2,}', '-', s).strip('-')


def slugify_no_repeat(slug, instance=None, slug_field='slug', filter_dict=None):
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (slug, counter)
            counter += 1
    return slug


def convert_price(product, currency):
    current_sale = product.get_current_sale()
    sale = 0
    price = product.get_price(currency)

    if current_sale:
        if current_sale.percentage:
            sale = price * current_sale.percentage / 100
        if current_sale.value:
            if current_sale.currency == currency:
                sale += current_sale.value
            else:
                sale += current_sale.value * currency.factor

    return Decimal(price - sale).quantize(Decimal('.01'), rounding=ROUND_UP)


def convert_price_usd(price_usd, currency):
    price = price_usd * currency.factor
    return Decimal(price).quantize(Decimal('.01'), rounding=ROUND_UP)
