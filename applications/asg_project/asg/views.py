# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from models import UserProfile, MaxHighScore, GameExperiment

from game import create_and_start_game, store_game, retrieve_game, end_game

from log import log_move_event

def index(request):
    context = RequestContext(request, {})
    return render_to_response('asg/index.html', context)

def pick(request):
    ge = GameExperiment.objects.all()
    context = RequestContext(request, {})
    return render_to_response('asg/pick.html', {'ge':ge}, context)

def leaderboard(request):
    context = RequestContext(request, {})
    up = UserProfile.objects.all().extra(select={ 'total' : 'total_points / no_games_played' }).order_by('-total')
    paginator = Paginator(up, 20)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    return render_to_response('asg/leaderboard.html', {'players': players}, context)

def startgame(request, num):
        context = RequestContext(request, {})
        session_id = request.session._get_or_create_session_key()
        game = create_and_start_game(int(num))
        data = game.get_game_state()
        store_game(session_id, game)
        response = render_to_response('asg/game.html', {'sid':session_id, 'data': data }, context)
        response.set_cookie('gid',session_id)
        return response

def query(request):
        context = RequestContext(request, {})
        gid = ''
        data = {}
        if request.COOKIES.has_key('gid'):
            gid = request.COOKIES['gid']
        game = retrieve_game(gid)
        if game:
            log_move_event(request.user.id, game)
            game.issue_query()
            store_game(gid, game)
            data = game.get_game_state()

        new_high = False
        if game.is_game_over():
            # check if this is a high score
            # update userprofile stats
            new_high = end_game(request.user, game)

        return render_to_response('asg/game.html', {'sid':gid, 'data': data, 'new_high':new_high}, context)

def assess(request):
        context = RequestContext(request, {})
        gid = ''
        if request.COOKIES.has_key('gid'):
            gid = request.COOKIES['gid']


        data = {}
        game = retrieve_game(gid)
        if game:
            game.examine_document()
            store_game(gid,game)
            data = game.get_game_state()

        new_high = False
        if game.is_game_over():
            # check if this is a high score
            # update userprofile stats
            new_high = end_game(request.user, game)

        return render_to_response('asg/game.html', {'sid':gid, 'data': data, 'new_high':new_high}, context)

def profile_page(request, username):
    context = RequestContext(request, {})
    user = User.objects.get(username=username)
    if user:
        user_profile = user.get_profile()
        high_scores = MaxHighScore.objects.filter(user=user)

        combined_points = 0
        mhs = MaxHighScore.objects.filter(user=user)
        for scores in mhs:
            combined_points = combined_points + scores.points

        user_profile.combined_points = combined_points

        return render_to_response('asg/profile.html', {'player': user,
                                                             'profile': user_profile,
                                                             'scores': high_scores, 'game_scores':mhs}, context)
    else:
        return HttpResponse('User not found')