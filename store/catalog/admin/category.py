# coding=utf-8
from tinymce.widgets import TinyMCE
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.translation import ugettext_lazy as _
from djantix.admin import make_active, make_not_active

from catalog.models import Category, CategoryImage


class CategoryImageInlineAdmin(admin.TabularInline):
    model = CategoryImage
    extra = 0


class CategoryAdmin(MPTTModelAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'name', ('is_active', 'ordering'), 'slug', 'short_description', 'description')}),
        (_("SEO"), {'fields': ('meta_keywords', 'meta_description')})
    )
    actions = [make_active, make_not_active]
    inlines = [CategoryImageInlineAdmin, ]
    list_display = ('name', 'external_slug', 'is_active')
    mptt_level_indent = 20

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(
                mce_attrs={
                    'height': "400",
                    'width': "600",
                },
            ))
        return super(CategoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(Category, CategoryAdmin)
