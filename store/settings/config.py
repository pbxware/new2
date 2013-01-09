# coding=utf-8
from livesettings.values import *
from django.utils.translation import ugettext_lazy as _
from livesettings import config_register_list

SITE_GROUP = ConfigurationGroup('template_blocks', _('Site Settings'), ordering=0)
config_register_list(
    LongStringValue(SITE_GROUP, 'title', description=_('Title'), ordering=1),
    LongStringValue(SITE_GROUP, 'meta_description', description=_('Meta Description'), ordering=1),
    LongStringValue(SITE_GROUP, 'meta_keywords', description=_('Meta Keywords'), ordering=1),
    LongStringValue(SITE_GROUP, 'footer', description=_('Footer'), ordering=1, default=""),

    PositiveIntegerValue(SITE_GROUP, 'refresh_interval_slider', description=_('Refresh Interval Slider'), default=1000),
)

'''
STORE_GROUP = ConfigurationGroup('store_groups', _('Store Settings'), ordering=0)
config_register_list(
    LongStringValue(STORE_GROUP, 'title', description=_('Title'), ordering=1),
    LongStringValue(STORE_GROUP, 'description', description=_('Description'), ordering=2),
    LongStringValue(STORE_GROUP, 'address', description=_('Address'), ordering=3),
    #LongStringValue(STORE_GROUP, 'meta_keywords', description=_('Meta Keywords'), ordering=1),
    #LongStringValue(SITE_GROUP, 'footer', description=_('Footer'), ordering=1, default=""),
)'''
