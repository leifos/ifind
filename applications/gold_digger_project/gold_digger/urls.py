from django.conf.urls import patterns, url
from gold_digger import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^about/$', views.about, name='about'),
        url(r'^leaderboards/$', views.leaderboards, name='home'),
        url(r'^register/$', views.register, name='register'),
        url(r'^user_login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^game/$', views.game, name='game'),
        url(r'^game_choice/$', views.game_choice, name='gamechoice'),
        url(r'^dig/$', views.dig, name='dig'),
        url(r'^move/$', views.move, name='move')

)