# coding=utf-8
from django.contrib import admin
from models import Order, OrderProduct, TrackOrder
from django.contrib.auth.models import User, Group
from delivery.CDEK.models import Delivery
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djantix.shortcuts import get_or_none


class OrderProductInlineAdmin(admin.TabularInline):
    model = OrderProduct
    raw_id_fields = ('product', )
    extra = 1


class DeliveryInlineAdmin(admin.StackedInline):
    model = Delivery
    extra = 1
    max_num = 1
    fieldsets = (
        (None, {'fields': ('tariff', 'bull_num', ('min_days', 'max_days', ),)}),
        (_('From'), {'fields': (('location_from', 'location_from_id'), )}),
        (_('To'), {'fields': (('location_to', 'location_to_id'), )}),
        (_('Price'), {'fields': (('price', 'currency'),)}),
    )


class TrackOrderInlineAdmin(admin.TabularInline):
    model = TrackOrder
    extra = 0
    #readonly_fields = ('performer', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'performer':
            kwargs['initial'] = request.user.id
            db_field.editable = False
        return db_field.formfield(**kwargs)


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    list_filter = ('status', 'manager', 'date_updated')
    list_display = ('__unicode__', 'status', 'summary', 'delivery_price')
    filter_horizontal = ('products', )
    inlines = (OrderProductInlineAdmin, DeliveryInlineAdmin, TrackOrderInlineAdmin)

    fieldsets = (
        (None, {'fields': ('status', 'owner', 'manager')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager" and getattr(settings, 'MANAGER_GROUP_NAME', None):
            group = get_or_none(Group, name=settings.MANAGER_GROUP_NAME)
            if group:
                kwargs['queryset'] = User.objects.filter(groups=group)
        return db_field.formfield(**kwargs)

    def save_formset(self, request, form, formset, change):
        if not formset.model == TrackOrder:
            return super(OrderAdmin, self).save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.performer = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(Order, OrderAdmin)


'''class TrackOrderAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'performer':
            kwargs['initial'] = request.user.id
        return db_field.formfield(**kwargs)
admin.site.register(TrackOrder, TrackOrderAdmin)'''
