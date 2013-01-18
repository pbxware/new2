# coding=utf-8
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField
from djantix.models import MPTTActiveTimeModel, ActiveTimeModel
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext_lazy as _
from catalog.utils import slugify, slugify_no_repeat


class Category(MPTTActiveTimeModel):
    name = models.CharField(_("Name"), max_length=100)

    slug = models.CharField(max_length=255, blank=True)
    external_slug = models.CharField(max_length=255, unique=True, editable=False, db_index=True)

    short_description = models.CharField(_('Short Description'), blank=True, max_length=250)
    description = HTMLField(_("Description"), blank=True)

    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'catalog'
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name

    def _get_mainimage(self):
        imgs = self.images.active().order_by('ordering')
        if len(imgs):
            return imgs[0]
        return ''
    main_image = property(_get_mainimage)

    def _generate_ext_slug(self, slug):
        if self.parent:
            return "/".join((self.parent.external_slug, slug))
        else:
            return slug

    @models.permalink
    def get_absolute_url(self):
        return ('store:category', (), {'slug': self.external_slug})

    def save(self, *args, **kwargs):
        #if self.parent:
        #    self.is_active = self.parent.is_active
        if not self.slug:
            self.slug = slugify_no_repeat(slugify(self.name), instance=self).lower()
        self.external_slug = self._generate_ext_slug(self.slug)
        super(Category, self).save(*args, **kwargs)
        for item in self._recurse_for_children(self):
            item.external_slug = item._generate_ext_slug(item.slug)
            item.save()



class CategoryImage(ActiveTimeModel):
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="images")
    image = ImageField(_("Image"), upload_to="store/categories", blank=True, null=True, storage=settings.UPLOAD_FILE_STORAGE)
    caption = models.CharField(_("Caption"), max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'catalog'
        verbose_name = _("Category Image")
        verbose_name_plural = _("Category Images")

    def __unicode__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if not self.caption:
            self.caption = self.image.name
        super(CategoryImage, self).save(*args, **kwargs)
