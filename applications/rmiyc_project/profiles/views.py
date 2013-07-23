# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from ifind.models.game_models import HighScore, PlayerAchievement, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
from django.forms import ModelForm
from forms import *
from configuration import MEDIA_URL
from django.contrib.auth.decorators import login_required


def profile_page(request, username):
    murl = MEDIA_URL
    context = RequestContext(request, {})
    u = User.objects.get(username=username)
    if u:
        user_profile = u.get_profile()
    if request.user == u:
        level = user_profile.level
        xp = user_profile.xp
        achievements = PlayerAchievement.objects.filter(user=u)
        for i in achievements:
            print MEDIA_URL + str(i.achievement.badge_icon)
            print i.achievement.badge_icon
        highscores = HighScore.objects.filter(user=u)
        view_permission = True
        return render_to_response('profiles/profile_page.html', {'user_profile': u,
                                                                 'profile': user_profile,
                                                                 'level':level,
                                                                 'murl': murl,
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
@login_required
def edit_profile(request, username):
    context = RequestContext(request, {})
    usr = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=usr)
    form = ProfileForm(instance=profile)
    if request.method == 'GET':
        return render_to_response('profiles/edit_profile.html', {'form': form}, context)
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            #usr = User.objects.get(username=username)
            #profile = UserProfile.objects.get(user=usr)
            profile.age = form.cleaned_data['age']
            profile.gender = form.cleaned_data['gender']
            profile.school = form.cleaned_data['school']
            profile.country = form.cleaned_data['country']
            profile.city = form.cleaned_data['city']
            profile.save()
        else:
            #say form invalid
            pass
        return profile_page(request,username)





