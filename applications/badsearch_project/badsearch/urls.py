from django.conf.urls import patterns, url
from badsearch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^search/', views.search, name='search'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^endexperiment/$', views.endexperiment, name='endexperiment'),
        )