# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from ifind.models import game_models
from django.contrib.auth import authenticate


def profile_page(request, profile_page):
    return HttpResponse("wassup")
    user_profile = request.user.get_profile()
    url = user_profile.url
    context = RequestContext(request)
    return render_to_response(url, {}, context)
