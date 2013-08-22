__author__ = 'leif'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
        url(r'^(?P<username>[a-zA-Z0-9_.+@-]+)/edit_profile', views.edit_profile),
        #url(r'^(?P<username>[a-zA-Z_.-]+)/graphs.html', views.graphs),
        url(r'^(?P<username>[a-zA-Z0-9_.+@-]+)', views.profile_page, name='profile'),

      )
