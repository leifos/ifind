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
from ifind.common.setuplogger import create_ifind_logger,get_ifind_logger
from datetime import datetime
import urllib, urllib2
import json
# Create your views here.


def index(request):
        context = RequestContext(request, {})
        #create the logger
        create_ifind_logger("Log")
        return render_to_response('rmiyc/index.html', context)


def play(request, category_name):
        create_ifind_logger("Log")
        context = RequestContext(request, {})
        #Create game avatar
        avatar = GameAvatar('GamePage')
        #Get the current user
        u = request.user
        # If the user is anonymous, then the user anon (added to db in population scripts) will be retrieved
        if not u.is_authenticated():
            u = User.objects.get(username='anon')
        else:
            avatar.update(request.user)

        #decode the category name to  replace '_' with ' '
        decoded_category_name= decode_url_to_string(category_name)
        #query the database for the provided category name
        c = Category.objects.get(name= decoded_category_name)
        #create game mechanics
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

            avatar.update(current_game=gm.game)
            msg = avatar.get()
            response = render_to_response('rmiyc/game.html', {'page': p.screenshot, 'avatar':msg ,'game_running':True, 'category':decoded_category_name}, context)
            response.set_cookie('game_id', game_id)
            # terminate the session whenever the browser closes
            #response.cookies.set_expiry(0)
            return response


def pick_category(request):
        context = RequestContext(request, {})
        #TODO(leifos): filter this
        cats = Category.objects.filter(is_shown=True)

        for c in cats:
            if request.user.is_authenticated():
                hs = HighScore.objects.filter(user=request.user ,category=c)
                if len(hs) >0:
                    c.score = hs[0].highest_score
                else:
                    c.score = 0
            else:
                c.score = 0

            c.url = encode_string_to_url(c.name)

        avatar = GameAvatar('CategoryPage')

        if request.user.is_authenticated():
            avatar.update(user=request.user)

        msg = avatar.get()
        response = render_to_response('rmiyc/cat_picker.html', {'cats': cats, 'avatar': msg}, context)
        response.delete_cookie('game_id')
        return response


def search(request):
        #get current user
        user = request.user
        result_list = []

        #create game avatar
        avatar = GameAvatar('Search')
        if request.user.is_authenticated():
            avatar.update(user=user)

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
                result_list = gm.get_search_results(query,top=10)

            gm.handle_query(query)
            gm.update_game()
            avatar.update(current_game=gm.game)
            # get the last query score
            objects = []
            for item in result_list:
                objects.append({"title": item.title, "link": item.url, "summary": item.summary})
            json_objects = json.dumps(objects)
            last_score = gm.get_last_query_score()
            current_score = gm.get_current_score()
            msg = avatar.get()
            if gm.is_game_over():
                gm.handle_game_over()
                Json_results = {
                    "results": json_objects, "score": last_score, "is_game_over": 1, "url_to_find":gm.get_current_page().url,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(), "current_score": current_score,
                    "avatar": msg
                }
            else:
                Json_results = {
                    "results": json_objects, "score": last_score, "is_game_over": 0, "url_to_find":gm.get_current_page().url,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(), "current_score": current_score,
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
    avatar = GameAvatar('Skip')
    if request.user.is_authenticated():
        avatar.update(user=user)

    if request.COOKIES.has_key('game_id'):
            ds = EngineFactory("bing", api_key=BING_API_KEY)
            gm = RMIYCMechanic(ds)
            game_id = request.COOKIES.get('game_id')
            gm.retrieve_game(user, game_id)
            gm.take_points()
            gm.set_next_page()
            gm.update_game()
            p = gm.get_current_page()
            current_score = gm.get_current_score()
            quoted_screenshot = str(p.screenshot)
            msg = avatar.get()
            if gm.is_game_over():
                gm.handle_game_over()
                objects = {
                    "screenshot": quoted_screenshot, "is_game_over": 1,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(), "current_score": current_score,
                    "avatar": msg
                    }
            else:
                objects = {
                    "screenshot": quoted_screenshot, "is_game_over": 0,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds(), "current_score": current_score,
                    "avatar": msg
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
    create_ifind_logger("Log")
    context = RequestContext(request, {})
    user = request.user
    if request.COOKIES.has_key('game_id'):
        game_id = request.COOKIES.get('game_id')
        ds = EngineFactory("bing", api_key=BING_API_KEY)
        gm = RMIYCMechanic(ds)
        gm.retrieve_game(user, game_id)
        statistics =[]
        statistics.append({'score': gm.get_current_score(), 'no_queries':gm.get_no_of_queries_issued(),
                           'no_successful_queries': gm.get_no_of_successful_queries_issued(), 'category':gm.get_game_category_name(),
                           'no_round': gm.get_final_round_no(), 'no_successful_round': gm.get_no_rounds_completed()})
        response = render_to_response('rmiyc/game_over.html',{'statistics': statistics}, context)
        response.delete_cookie('game_id')
        return response
    else:
        return render_to_response('rmiyc/game_over.html', context)



def about(request):
    context = RequestContext(request, {})
    return render_to_response('rmiyc/about.html', context)
