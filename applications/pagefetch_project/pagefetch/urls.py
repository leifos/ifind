__author__ = 'leif'

from django.conf.urls import patterns, url, include
from pagefetch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^play/(?P<category_name>\w+)', views.play, name='play'),
        url(r'^pick_category/$', views.pick_category, name='pick_category'),
        url(r'^search/$', views.search, name='search'),
        url(r'^about/$', views.about, name='about'),
        url(r'^search/$', views.search, name='search'),
        url(r'^game_over/$', views.game_over, name='game_over'),
        url(r'^display_next_page/$', views.display_next_page, name='display_next_page'),
)
