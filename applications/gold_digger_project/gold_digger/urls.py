from django.conf.urls import patterns, url
from gold_digger import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^about/$', views.about, name='about'),
        url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
        url(r'^register/$', views.register, name='register'),
        url(r'^user_login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^move/$', views.move, name='move'),
        url(r'^game_over/$', views.game_over, name='game_over'),
        url(r'^back_to_main/$', views.back_to_main, name='back_to_main'),
        url(r'^game_choice2/$', views.game_choice2, name='game_choice2'),
        url(r'^profile/$', views.user_profile, name='profile'),
        url(r'^game2/$', views.game2, name='game2'),
        url(r'^ajaxview/$', views.ajaxview, name='ajaxview'),
        url(r'^store/$', views.store, name='store'),
        # url(r'^ajax_buy/$', views.ajax_buy, name='store'),
        url(r'^update_location/$', views.update_location, name='update_location'),
        url(r'^tour/$', views.tour, name='tour'),
        url(r'^update_cost/$', views.update_cost, name='update_cost'),
        url(r'^ajax_upgrade/$', views.ajax_upgrade, name='ajax_upgrade'),
        url(r'^ajax_exit/$', views.ajax_exit, name='exit'),
        url(r'^game_over2/$', views.game_over2, name='game_over2'),
        url(r'^achievements/$', views.achievements, name='achievements'),
        url(r'^display_achievements/$', views.display_achievements, name='display_achievements'),
        url(r'^egg/$', views.egg, name='egg')


)