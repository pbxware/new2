# coding=utf-8
import re
from django import template
from django.template.defaultfilters import stringfilter

from django.utils.functional import allow_lazy
from django.utils.encoding import force_unicode

register = template.Library()


def strip_tags_space(value):
    return re.sub(r'<[^>]*?>', ' ', force_unicode(value))
strip_tags = allow_lazy(strip_tags_space)


@register.filter
@stringfilter
def noramlize(text):
    normalized_text = strip_tags_space(text).replace('\n', ' ')
    return ' '.join(normalized_text.split())
