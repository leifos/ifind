# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def test(request):
    context = RequestContext(request)
    return render_to_response('pagefetch/test.html', {}, context)

def index(request):
    pass

def leaderboard(request):
    pass

def game_start(request, category_id):

    # create game mechanic object to initialize game

    # add game_id to session/cookie
    pass

def game_show_cat(request):

    # get the categories for the game chosen

    pass

def game_end(request):

    #

    pass

def game_handle_search(request):

    # get game_id

    # create game_mechnic and retrieve game with game_id

    # log the query issued

    pass

def game_next_page(request):

    # get game_id

    # create game_mechnic and retrieve game with game_id

    # log the game state, page, and outcome

    pass

def game_quit(request):
    pass




