# coding=utf-8
from django.db import models


class ActiveManager(models.Manager):
    def active(self, *args, **kwargs):
        return self.filter(is_active=True, *args, **kwargs)
