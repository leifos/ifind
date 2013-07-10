from django.conf.urls import patterns, include, url
from settings import DEBUG
#from settings import MEDIA_ROOT
from settings import DEPLOY


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pagefetch_project.views.home', name='home'),
    # url(r'^pagefetch_project/', include('pagefetch_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pf/', include('pagefetch.urls')),
    #url(r'^', include('pagefetch.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^users/', include('pagefetch.urls')),
)


#if DEBUG and not DEPLOY:
#    urlpatterns += ('django.views.static',(r'media/(?P<path>.*)', 'serve', {'document_root': MEDIA_ROOT}),)

