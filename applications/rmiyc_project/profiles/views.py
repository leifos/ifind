# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from ifind.models.game_models import HighScore, PlayerAchievement
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def profile_page(request, username):
    context = RequestContext(request, {})
    u = User.objects.get(username=username)
    if u:
        user_profile = u.get_profile()
    if request.user == u:
        level = user_profile.level
        xp = user_profile.xp
        achievements = PlayerAchievement.objects.filter(user=u)
        highscores = HighScore.objects.filter(user=u)
        view_permission = True
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'profile': user_profile,
                                                                 'level':level,
                                                                 'age':user_profile.age,
                                                                 'achievements': achievements,
                                                                 'view_perm': view_permission,
                                                                 'highscores': highscores,
                                                                 'xp':xp}, context)
    else:
        view_permission = False
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'view_perm': view_permission,
                                                                 'profile': user_profile},
                                                                  context)
