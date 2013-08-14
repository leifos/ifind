from django.conf.urls import url
from django.conf.urls import patterns

from . import views

urlpatterns = patterns('search.views',
    url(r'^$', views.IndexView),
    url(r'^search/$', views.search),
    url(r'^session/$', views.session),
)