__author__ = 'leif'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
        url(r'^$', views.leaderboards, name='leaderboards'),
      )