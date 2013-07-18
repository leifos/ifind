# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def leaderboards(request):
    context = RequestContext(request, {})
    return render_to_response('leaderboard/leaderboard.html', context)



