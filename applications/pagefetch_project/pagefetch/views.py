# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from ifind.models import game_models
from django.contrib.auth import authenticate


#@login_required
def user_profile(request):
    #request.session.flush()
    #user_profile = request.user.get_profile()
    #url = user_profile.url
    #context = RequestContext(request)
    #return render_to_response(url, {}, context)
    user = request.user
    print user
    if request.user.is_authenticated():
        #test this works how i think it should..
        return HttpResponse("hello " + str(request.user) + '<a href="/accounts/logout/">log out</a>')
    else:
        return HttpResponse("not logged in")
   # return HttpResponse("wassup")


def logout(request):
    logout(request)

def login(request):
    #new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
    login(request)
    return user_profile(request)


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





    return HttpResponse("wassup")
