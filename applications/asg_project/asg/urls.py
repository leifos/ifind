__author__ = 'leif'

from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^start/', views.startgame, name='startgame'),
        url(r'^query/$', views.query, name='query'),
        url(r'^assess/$', views.assess, name='assess'),

)