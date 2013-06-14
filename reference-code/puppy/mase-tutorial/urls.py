from django.conf.urls.defaults import *
from django.conf import settings

from settings import ONDOLLEMAN

def killit(request):
	assert False

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^interface/', include('interface.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    
    (r'^mase/$', 'mase.views.index'),
    
)

if ONDOLLEMAN:
    urlpatterns += patterns('', url(r'^site_media/(?P<path>.*)$', killit), url(r'^<mase_tutorial>.*site_media/.*$', killit))
    urlpatterns += patterns('', url(r'^mase-tutorial/$', 'mase.views.index'))
else:
    urlpatterns += patterns('', url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }))
 

 
