__author__ = 'leif'

from django.conf.urls import patterns, url, include
from pagefetch import views

urlpatterns = patterns('',
    url(r'^$',views.user_profile),
)
