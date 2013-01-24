# coding=utf-8
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import importlib


class Command(BaseCommand):
    help = 'Update cities list'

    def handle(self, *args, **options):
        delivery_backend = importlib.import_module(settings.BACKEND_DELIVERY)
        func = delivery_backend.run
        func()
