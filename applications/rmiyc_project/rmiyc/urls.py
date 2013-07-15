from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^play/(?P<category_name>\w+)', views.play, name='play'),
        url(r'^pick_category/$', views.pick_category, name='pick_category'),
        #url(r'^search/$', views.search, name='search'),
        url(r'^search/$', views.search2, name='search2'),
        url(r'^game_over/$', views.game_over, name='game_over'),
        #url(r'^display_next_page/$', views.display_next_page, name='display_next_page'),
        url(r'^display_next_page/$', views.display_next_page2, name='display_next_page'),
)