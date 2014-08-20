from django.conf.urls import patterns, include, url
from django.conf import  settings
from django.views.generic.base import  RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gold_digger_project.views.home', name='home'),
    # url(r'^gold_digger_project/', include('gold_digger_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url= "/gold_digger/")),
    url(r'^gold_digger/', include('gold_digger.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}),)