# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from ifind.models.game_leaderboards import HighScoresLeaderboard, CatHighScoresLeaderboard


def leaderboards(request):
    context = RequestContext(request, {})
    high_scores = HighScoresLeaderboard().get_leaderboard()
    cat_high_scores = CatHighScoresLeaderboard().get_leaderboard()

    return render_to_response('leaderboard/leaderboard.html', {'high_scores':high_scores, 'cat_high_scores':cat_high_scores}, context)



