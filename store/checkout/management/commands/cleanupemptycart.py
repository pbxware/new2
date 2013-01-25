# coding=utf-8
from django.core.management.base import NoArgsCommand
from cart.models import Cart


class Command(NoArgsCommand):
    help = 'Drop empty cart in store'

    def handle_noargs(self, **options):
        carts = Cart.objects.all()
        for cart in carts:
            if not len(cart.item_set.all()):
                cart.delete()
