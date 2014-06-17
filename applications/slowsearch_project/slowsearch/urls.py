__author__ = 'Craig'
from django.conf.urls import patterns, url
from slowsearch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'about/$', views.about, name='about'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
        url(r'^results/$', views.results, name='results'),
        url(r'^endexperiment/$', views.endexperiment, name='endexperiment'),
        # url(r'^survey/(<?P<surveyid>\w+)/$', views.survey, name='survey'),
        url(r'^search/$', views.search, name='search'),
        url(r'^finalsurvey/$', views.final_survey, name='finalsurvey'),
        )