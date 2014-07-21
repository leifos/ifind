from django.conf.urls import patterns, url
from gold_digger import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^about/$', views.about, name='about'),
        url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
        url(r'^register/$', views.register, name='register'),
        url(r'^user_login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^dig/$', views.dig, name='dig'),
        url(r'^move/$', views.move, name='move'),
        url(r'^game_over/$', views.game_over, name='game_over'),
        url(r'^back_to_main/$', views.back_to_main, name='back_to_main'),
        url(r'^shop/$', views.shop, name='shop'),
        url(r'^buy/$', views.buy, name='buy'),
        url(r'^game_choice2/$', views.game_choice2, name='game_choice2'),
        url(r'^profile/$', views.user_profile, name='profile'),
        url(r'^game2/$', views.game2, name='game2'),
        url(r'^ajaxview/$', views.ajaxview, name='ajaxview')




)