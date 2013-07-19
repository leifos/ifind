from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from ifind.search.engine.bing import
from ifind.search.query import Query
from keys import BING_API_KEY
from ifind.models.game_mechanics import GameMechanic
from ifind.models.game_models import Category, Page, HighScore ,CurrentGame
from ifind.models.game_avatar import GameAvatar
from django.contrib.auth.models import User
from ifind.search import EngineFactory
from rmiyc_mechanics import RMIYCMechanic
from ifind.common.utils import encode_string_to_url, decode_url_to_string
from datetime import datetime
import urllib, urllib2
import json
# Create your views here.

def index(request):
        context = RequestContext(request, {})
        return render_to_response('rmiyc/index.html', context)

def play(request, category_name):
        # Get the current user
        context = RequestContext(request, {})

        avatar = GameAvatar('GamePage')

        u = request.user
        # If the user is anonymous, then a new user will be created
        if not u.is_authenticated():
            u = User.objects.get(username='anon')
        else:
            avatar.update(user=u)

        # Query the database for the provided category name

        c = Category.objects.get(name=decode_url_to_string(category_name))

        gm = RMIYCMechanic()
        # This view shall be called when a new game is to start
        # Thus, there should be no cookie containing a game_id
        if request.COOKIES.has_key('game_id'):
            # redirect the player to the page where they can pick a category and start a new game
            response = HttpResponseRedirect('/rmiyc/pick_category/')
            # delete the cookie
            response.delete_cookie('game_id')
            return response
        else:
            # create a new game
            gm.create_game(u, c, 0)
            # get the game_id to assign it later to a cookie
            game_id = gm.get_game_id()
            # get the current page that is going to be displayed first to the user
            p = gm.get_current_page()
            # initiate the array which will hold all the result list, the page that is going to be shown and the score

            avatar.update(current_game=gm.game)

            msg = avatar.get()

            overall_results = []
            overall_results.append({
                    'result_list': [], 'page': p.screenshot, 'score': 0 ,
                    'no_round': gm.get_round_no(), 'no_successful_round': gm.get_no_rounds_completed(),
                    'no_of_queries_issued_for_current_page': gm.get_no_of_queries_issued_for_current_page(),
                    'no_remaining_rounds': gm.get_remaining_rounds()
            })
            response = render_to_response('rmiyc/game.html', {'overall_results': overall_results, 'avatar':msg}, context)
            response.set_cookie('game_id', game_id)
            # terminate the session whenever the browser closes
            #response.cookies.set_expiry(0)




            return response


def pick_category(request):
        context = RequestContext(request, {})
        scores=[]

        #TODO(leifos): filter this
        cats = Category.objects.filter(is_shown=True)

        for c in cats:
            c.score = 0
            c.url = encode_string_to_url(c.name)

        avatar = GameAvatar('CategoryPage')
        if request.user:
            avatar.update(user=request.user)

        if request.user.is_authenticated():
            #TODO(leifos):  get the users high score and update the cats
            hs = HighScore.objects.filter(user=request.user)


        msg = avatar.get()

        return render_to_response('rmiyc/cat_picker.html', {'cats': cats, 'avatar': msg}, context)


def search(request):

        user = request.user
        result_list = []

        avatar = GameAvatar('Search')
        if user != 'anon':
            avatar.update(user=user)

        msg = avatar.get()


        if request.COOKIES.has_key('game_id'):
            ds = EngineFactory("bing", api_key=BING_API_KEY)
            gm = RMIYCMechanic(ds)
            game_id = request.COOKIES.get('game_id')
            gm.retrieve_game(user, game_id)
            if request.method == 'GET':
                query = request.GET['query'].strip()
                #Augement query
                query += ' site:gla.ac.uk '
            if query:

                result_list = gm.get_search_results(query)

            gm.handle_query(query)
            gm.update_game()
            # get the last query score
            objects = []
            for item in result_list:
                objects.append({"title": item.title, "link": item.url, "summary": item.summary})
            json_objects = json.dumps(objects)
            s = gm.get_last_query_score()
            if gm.is_game_over():
                Json_results = {
                    "results": json_objects, "score": s, "is_game_over": 1,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(),
                    "avatar": msg
                }
            else:
                Json_results = {
                    "results": json_objects, "score": s, "is_game_over": 0,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(),
                    "avatar": msg
                }
            data = json.dumps(Json_results)
            return HttpResponse(data, mimetype='application/json')
        else:
            # the game has not been created yet
            # redirect to play view
            return HttpResponseRedirect('/rmiyc/cat_picker/')


def display_next_page(request):

    user = request.user
    if request.COOKIES.has_key('game_id'):
            ds = EngineFactory("bing", api_key=BING_API_KEY)
            gm = RMIYCMechanic(ds)
            game_id = request.COOKIES.get('game_id')
            gm.retrieve_game(user, game_id)
            gm.take_points()
            gm.set_next_page()
            gm.update_game()
            p = gm.get_current_page()
            quoted_screenshot = str(p.screenshot)
            if gm.is_game_over():
                objects = {
                    "screenshot": quoted_screenshot, "is_game_over": 1,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds()
                    }
            else:
                objects = {
                    "screenshot": quoted_screenshot, "is_game_over": 0,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds()
                }
            data = json.dumps(objects)
            return HttpResponse(data, mimetype='application/json')
    else:
            # the game has not been created yet
            # redirect to play view
            print 'the game has not been created yet'
            return HttpResponseRedirect('/rmiyc/cat_picker/')


def game_over(request):
    print 'I am a cookie and I am dying because the game is over'
    context = RequestContext(request, {})
    user = request.user
    if request.COOKIES.has_key('game_id'):
        game_id = request.COOKIES.get('game_id')
        ds = EngineFactory("bing", api_key=BING_API_KEY)
        gm = RMIYCMechanic(ds)
        game = gm.retrieve_game(user, game_id)
        statistics =[]
        statistics.append({'score': gm.get_current_score(), 'no_queries':gm.get_no_of_queries_issued(),
                           'no_successful_queries': gm.get_no_of_successful_queries_issued(),
                           'no_round': gm.get_final_round_no(), 'no_successful_round': gm.get_no_rounds_completed()})
        response = render_to_response('rmiyc/game_over.html',{'statistics': statistics}, context)
        response.delete_cookie('game_id')
        return response


