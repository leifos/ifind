__author__ = 'leif'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
        url(r'^(?P<username>\w+)/edit_profile', views.edit_profile),
        url(r'^(?P<username>\w+)/graphs.html', views.graphs),
        url(r'^(?P<username>\w+)', views.profile_page, name='profile'),

      )
