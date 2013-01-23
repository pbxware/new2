# coding=utf-8
from tinymce.widgets import TinyMCE
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from djantix.admin import make_active, make_not_active
from django.forms import models, ValidationError
from catalog.models.product import Product, Sale, ProductImage, ProductFile, ProductScreenshot, ProductAttributeValue, ProductAttribute
from catalog.validations import validate_attribute_value
from django import forms


def clean_attribute_value(cleaned_data, obj):
    value = cleaned_data['value']
    attribute = cleaned_data['attribute']
    success, valid_value = validate_attribute_value(attribute, value, obj)
    if not success:
        raise ValidationError(_("Invalid Entry"))
    return valid_value


class ProductImageInlineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductFileInlineAdmin(admin.TabularInline):
    model = ProductFile
    extra = 0


class ProductScreenshotInlineAdmin(admin.TabularInline):
    model = ProductScreenshot
    extra = 0


class ProductAttributeInlineForm(models.ModelForm):
    def clean_value(self):
        return clean_attribute_value(self.cleaned_data, self.cleaned_data['product'])


class ProductAttributeInlineAdmin(admin.TabularInline):
    form = ProductAttributeInlineForm
    model = ProductAttributeValue
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'full_name')
    list_filter = ('category', 'is_published', 'is_active', 'is_new', 'is_featured')
    filter_horizontal = ('category', 'also_buy', 'analog', 'modification', 'adding_product')
    list_display = ('name', 'slug', 'date_added', 'date_updated', 'price', 'currency', 'items_in_stock')
    actions = [make_active, make_not_active]
    inlines = (
        ProductAttributeInlineAdmin,
        #ProductBrandInlineAdmin,
        ProductImageInlineAdmin,
        ProductScreenshotInlineAdmin,
        ProductFileInlineAdmin,
        #YCatalogProductInlineAdmin
    )
    fieldsets = (
        (None, {'fields': ('name', 'full_name', ('is_published', 'is_active', 'is_new', 'is_featured'), 'category', 'slug')}),

        (None, {'fields': (('price', 'currency'), 'items_in_stock'), }),
        (_('Relations'), {'fields': ('also_buy', 'analog', 'modification', 'adding_product'), }),

        (None, {'fields': ('short_description', 'description', 'guarantee')}),
        (_('Item Dimensions'), {'fields': (
            ('length', 'width', 'height'),
            ('weight', )
            ), 'classes': ('collapse', )}),
        (_("SEO"), {'fields': ('meta_keywords', 'meta_description')})
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(
                mce_attrs={
                    'height': "500",
                    'width': "600",
                    'content_css': settings.MEDIA_URL + 'css/tiny_mce/product.css'
                },
            ))
        return super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(Product, ProductAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
admin.site.register(ProductAttribute, ProductAttributeAdmin)


class SaleFormAdmin(forms.ModelForm):
    class Meta:
        model = Sale

    def clean(self, *args, **kwargs):
        percentage = self.cleaned_data.get('percentage')
        value = self.cleaned_data.get('value')
        if not (value or percentage):
            raise forms.ValidationError("Sale not available")
        return self.cleaned_data


class SaleAdmin(admin.ModelAdmin):
    form = SaleFormAdmin
    filter_horizontal = ('products', 'categories')
    fieldsets = (
        (None, {'fields': (('title', 'date_expiry',),)}),
        (_('Sale'), {'fields': ('percentage', ('value', 'currency'),)}),
        (_('Targets'), {'fields': ('products',)}),
        #(_('Targets'), {'fields': ('products', 'categories',)}),
    )
admin.site.register(Sale, SaleAdmin)
