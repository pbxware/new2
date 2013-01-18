# coding=utf-8
import os
from common_settings import *

TINYMCE_JS_URL = STATIC_URL + 'tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, 'tiny_mce')

TINYMCE_DEFAULT_CONFIG = {
    'width': "1024",
    'height': "600",
    'plugins': "table,media,advlink,advimage,spellchecker",
    'theme': "advanced",
    'mode': "exact",
    'font_size_style_values': "8px,10px,12px,14px,18px,24px,36px",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_disable': "",
    'gecko_spellcheck': 'true',

    'convert_urls': 'false',
    'relative_urls': 'false',
    'remove_script_host': 'false',

    'content_css': MEDIA_URL + 'css/tiny_mce/main.css',
    'theme_advanced_buttons1': "newdocument,cut,copy,paste,cleanup,removeformat,separator,undo,redo,separator,table,image,media,separator,link,unlink,anchor,separator,spellchecker,code",
    'theme_advanced_buttons2': "styleselect,formatselect,fontselect,fontsizeselect,separator,bold,italic,underline,strikethrough,separator,justifyright,justifycenter,justifyleft,justifyfull,separator,backcolor,forecolor",
    'theme_advanced_buttons3': "bullist,numlist,separator,hr,sub,sup,separator,outdent,indent,separator,charmap,visualaid,tablecontrols",
    'spellchecker_languages': '+Русский=ru,English=en',
    'style_formats': [
        #{'title': 'Info text', 'inline': 'span', 'classes': 'info-text'},
        #{'title': 'Comment text', 'inline': 'span', 'classes': 'comment-text'} ,
        {'title': 'Fancy Box', 'inline': 'a', 'classes': 'fancybox'},
    ]
}

FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + '/filebrowser/'
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_MEDIA_ROOT = STATIC_ROOT
FILEBROWSER_MEDIA_URL = STATIC_URL

INSTALLED_APPS += (
    'tinymce',
    #'filebrowser',
)
