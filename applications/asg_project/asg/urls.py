__author__ = 'leif'

from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^start/(?P<num>[0-9]+)/$', views.startgame, name='startgame'),
        url(r'^pick/', views.pick, name='pick'),

        url(r'^query/$', views.query, name='query'),
        url(r'^assess/$', views.assess, name='assess'),
        url(r'^(?P<username>[a-zA-Z0-9_.+@-]+)', views.profile_page, name='profile'),
)