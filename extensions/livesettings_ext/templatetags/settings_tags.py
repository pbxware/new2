# coding=utf-8
import livesettings
from django import template

register = template.Library()


@register.simple_tag
def settings_value(group, key):
    try:
        return livesettings.config_value(group, key)
    except livesettings.SettingNotSet:
        return ''
