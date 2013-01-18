# coding=utf-8
from django.conf.urls import patterns, include, url
#from filebrowser.sites import site
from django.conf import settings
from django.contrib import admin
#from cms.sitemaps import CMSSitemap
#from catalog.sitemaps import CategorySitemap, ProductSitemap

#tmp
#from django.views.generic.simple import direct_to_template

admin.autodiscover()

#sitemaps = {
#    'cmspages': CMSSitemap,
#    'category': CategorySitemap,
#    'products': ProductSitemap
#}

urlpatterns = patterns('',
    # admin
    #url(r'^admin/filebrowser/', include(site.urls)),  # filebrowser
    url(r'^admin/settings/', include('livesettings.urls')),  # livesettings
    #url(r'^admin/rosetta/', include('rosetta.urls')),  # rosetta
    #url(r'^admin/cache/', include('cache_utils.urls', namespace='cache')),  # cache_utils urls
    url(r'^admin/', include(admin.site.urls)),  # Djnago admin
    # extension
    #url(r'^tinymce/', include('tinymce.urls')),  # tinymce
    #url(r'^admin_tools/', include('admin_tools.urls')),  # admin tools
    #url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw'),
    #url(r'^extensions/', include('extensions.urls')),
    # site
    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    #url(r'^search', include('store.search.urls', namespace='search')),
    #url(r'^accounts/', include('account.urls', namespace='account')),  # registration
    #url(r'^checkout/', include('store.checkout.urls', namespace='checkout')),
    #url(r'^delivery/', include('delivery.urls')),  # location
    #url(r'^shop/', include('store.shop.urls', namespace='shop')),
    #url(r'^', include('cms.urls')),  # dkjango cms

    url(r'^store/', include('store.catalog.urls', namespace='store')),


    #url(r'^$', direct_to_template, {
    #    'template': 'index.jade'
    #}),
    #url(r'^store/$', direct_to_template, {
    #    'template': 'store/index.jade'
    #}),
    #url(r'^store/cat$', direct_to_template, {
    #    'template': 'store/category.jade'
    #}),
    #url(r'^store/cat/prods$', direct_to_template, {
    #    'template': 'store/products.jade'
    #}),
    #url(r'^store/cat/prod$', direct_to_template, {
    #    'template': 'store/product.jade'
    #}),
    #url(r'^store/nav$', direct_to_template, {
    #    'template': 'store/navigator.jade'
    #}),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
