__author__ = 'Craig'
from django.conf.urls import patterns, url
from slowsearch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'about/$', views.about, name='about'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout')
        )