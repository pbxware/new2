# coding=utf-8
from django.db import models

class City(models.Model):
    city_code = models.PositiveIntegerField()
    city_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.city_name
