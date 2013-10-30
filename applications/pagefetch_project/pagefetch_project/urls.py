from django.conf.urls import patterns, include, url
from settings import DEBUG
#from settings import MEDIA_ROOT
from settings import DEPLOY
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pagefetch import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pagefetch_project.views.home', name='home'),
    # url(r'^pagefetch_project/', include('pagefetch_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^pf/', include('pagefetch.urls')),
    #url(r'^', include('pagefetch.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/logout',views.logout),
    #url(r'^accounts/login', include('registration.backends.simple.urls')),
    #url(r'^users/', include('pagefetch.urls')),
    #url(r'^users/', views.user_profile),
    #url(r'', views.user_profile),
    url(r'^users/', include('profiles.urls')),
    url(r'^pagefetch/', include('pagefetch.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/register/$', MyRegistrationView.as_view(),name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^leaderboard/', include('leaderboard.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'', include('pagefetch.urls')),
)


#if DEBUG and not DEPLOY:
#    urlpatterns += ('django.views.static',(r'media/(?P<path>.*)', 'serve', {'document_root': MEDIA_ROOT}),)

if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'data/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

