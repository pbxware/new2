# coding=utf-8
from django.conf import settings
from django.db import models
from tinymce.models import HTMLField
from djantix.models import ActiveTimeModel
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext_lazy as _
from catalog.utils import slugify, slugify_no_repeat
from currencies.models import Currency
from category import Category


class Product(ActiveTimeModel):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True,)
    slug = models.CharField(max_length=255, unique=True, blank=True, db_index=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name=_("Category"), related_name="products")

    short_description = models.TextField(_('Short Description'), blank=True)
    description = HTMLField(_("Description"), blank=True)

    attribute = models.ManyToManyField('ProductAttribute', through='ProductAttributeValue')

    is_featured = models.BooleanField(_("Featured"), default=False)
    is_new = models.BooleanField(_("New"), default=True)
    is_published = models.BooleanField(_("Published"), default=True)

    guarantee = models.CharField(_("Guarantee"), max_length=255, blank=True, null=True,)

    weight = models.DecimalField(_("Weight"), max_digits=8, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(_("Length"), max_digits=6, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(_("Width"), max_digits=6, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(_("Height"), max_digits=6, decimal_places=2, null=True, blank=True)

    price = models.DecimalField(_("Price"), max_digits=14, decimal_places=6)
    currency = models.ForeignKey(Currency)

    items_in_stock = models.DecimalField(_("Number in stock"), max_digits=18, decimal_places=6, default='0')

    also_buy = models.ManyToManyField('self', blank=True, verbose_name=_("Also Buy"), related_name="also_buy")
    analog = models.ManyToManyField('self', blank=True, verbose_name=_("Analog"), related_name="analog")
    modification = models.ManyToManyField('self', blank=True, verbose_name=_("Modification"), related_name="modification")
    adding_product = models.ManyToManyField('self', blank=True, verbose_name=_("Adding"), related_name="adding")

    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'catalog'
        ordering = ('name',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def _get_mainimage(self):
        imgs = self.images.active().order_by('ordering')
        if len(imgs):
            return imgs[0]
    main_image = property(_get_mainimage)

    def _get_mainCategory(self):
        cats = self.category.active()
        if cats:
            return cats[0]
    main_category = property(_get_mainCategory)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_no_repeat(slugify(self.name), instance=self).lower()
        super(Product, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('store:show_product', (), {'slug_pro': self.slug})


class ProductAttribute(models.Model):
    VALIDATIONS = [
        ('validation_simple', _('One or more characters')),
        ('validation_integer', _('Integer number')),
        ('validation_yesno', _('Yes or No')),
        ('validation_decimal', _('Decimal number')),
    ]

    name = models.CharField(_("Name"), max_length=100)
    description = models.CharField(_("Description"), max_length=255)
    validation = models.CharField(_("Field Validations"), choices=VALIDATIONS, max_length=100)
    attribute_units = models.CharField(_("Attribute units"), max_length=3, null=True, blank=True)
    ordering = models.IntegerField(_("Ordering"), default=0)

    class Meta:
        app_label = 'catalog'
        verbose_name = _("Product attribute")
        verbose_name_plural = _("Product attributes")

    def __unicode__(self):
        if self.attribute_units:
            return '%s (%s)' % (self.description, self.attribute_units)
        return self.description


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="attributes")
    attribute = models.ForeignKey(ProductAttribute)
    value = models.CharField(max_length=255)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.attribute.description


class ProductImage(ActiveTimeModel):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="images")
    image = ImageField(upload_to="store/products", storage=settings.UPLOAD_FILE_STORAGE)
    caption = models.CharField(_("Caption"), max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        if not self.caption:
            self.caption = self.product.name
        super(ProductImage, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.image.name


class ProductScreenshot(ActiveTimeModel):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="screenshot")
    image = ImageField(upload_to="store/screenshots", storage=settings.UPLOAD_FILE_STORAGE)
    caption = models.CharField(_("Caption"), max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        if not self.caption:
            self.caption = self.image.name
        super(ProductScreenshot, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.image.name


class ProductFile(ActiveTimeModel):
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="file")
    file = models.FileField(upload_to="store/files", storage=settings.UPLOAD_FILE_STORAGE)
    caption = models.CharField(_("Caption"), max_length=255, blank=True, null=True)
    
    class Meta:
        app_label = 'catalog'
    
    def save(self, *args, **kwargs):
        if not self.caption:
            self.caption = self.file.name
        super(ProductFile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.file.name
