# coding=utf-8
import os
from django.core.files.storage import FileSystemStorage

_ = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

TIME_ZONE = 'Europe/Moscow'

LANGUAGES = (
    ('ru', _('Russian')),
)

LANGUAGE_CODE = 'ru'
DEFAULT_LANGUAGE = 'ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
MEDIA_URL = STATIC_URL + 'media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

UPLOAD_ROOT = os.path.join(STATIC_ROOT, 'uploads')
UPLOAD_URL = STATIC_URL + 'uploads/'

UPLOAD_FILE_STORAGE = FileSystemStorage(location=UPLOAD_ROOT, base_url=UPLOAD_URL)

SECRET_KEY = 'ud6kuo6syqjb%)a_3#=z!r(h7t-*5nny4kd-vhzskn0i42(ote'

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
    #'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    #'simple404log.middleware.Fallback404Middleware',
    #'bust_detector.middleware.BustDetector',
    #"threaded_multihost.middleware.ThreadLocalMiddleware",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    #'cache_utils.context_processors.timeout',
]

ROOT_URLCONF = 'store.urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'store', 'templates'),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.admin',

    'djantix',
    'sekizai',
    'livesettings',
    'livesettings_ext',
    'treemenus',
    'sorl.thumbnail',
    'mptt',
    'store',

    #'simple404log',
    #'keyedcache',
    #'sorl.thumbnail',
    #'djantix',
    #'rosetta',
    #'ya_catalog',
    #'oot'
    #'memcache_status',
    #'django_extensions'
]

#AUTH_PROFILE_MODULE = 'account.Profile'

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

#THUMBNAIL_DEBUG = True
# bust detector
#FORM_BUST_INTERVAL = 60
#FORM_BUST_COUNT = 3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
