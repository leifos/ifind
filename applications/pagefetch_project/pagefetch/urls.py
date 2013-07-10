__author__ = 'leif'

from django.conf.urls import patterns, url
from pagefetch import views


urlpatterns = patterns('',
    url(r'^$', views.test, name='test'),
)
