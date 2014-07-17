__author__ = 'Craig'
from django.conf.urls import patterns, url
from slowsearch import views
import django.contrib.auth.views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'about/$', views.about, name='about'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', django.contrib.auth.views.logout, {'template_name':'slowsearch/logged_out.html'}),
        url(r'^logged_out/$', views.logout, name='logged_out'),
        url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
        url(r'^editprofile/(?P<username>\w+)/$', views.editprofile, name='editprofile'),
        url(r'^results/(?P<page>\d+)/$', views.results, name='results'),
        url(r'^endexperiment/$', views.endexperiment, name='endexperiment'),
        # url(r'^survey/(<?P<surveyid>\w+)/$', views.survey, name='survey'),
        url(r'^search/$', views.search, name='search'),
        url(r'^finalsurvey/$', views.final_survey, name='finalsurvey'),
        url(r'^demographic/$', views.demographic, name='demographic'),
        url(r'^goto/(.*)/(.*)/$', views.goto, name='goto'),
        )