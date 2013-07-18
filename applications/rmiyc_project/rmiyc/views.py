from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
#from ifind.search.engine.bing import
from ifind.search.query import Query
from keys import BING_API_KEY
from ifind.models.game_mechanics import GameMechanic
from ifind.models.game_models import Category, Page, HighScore ,CurrentGame, UserProfile
from ifind.models.game_avatar import GameAvatar
from django.contrib.auth.models import User
from ifind.search import EngineFactory
from rmiyc_mechanics import RMIYCMechanic
from datetime import datetime
import urllib, urllib2
import json
# Create your views here.

def index(request):
        context = RequestContext(request, {})
        return render_to_response('rmiyc/index.html', context)

def play(request, category_name):
        # Get the current user
        username = request.user

        u = User.objects.get(username=username)

        if u is None:
            u = User.objects.get(username='anon')

        #####################

        avatar = GameAvatar('GamePage', user=u)
        print avatar.send()

        ####################


        # Query the database for the provided category name
        c = Category.objects.get(name=category_name)
        gm = RMIYCMechanic()
        context = RequestContext(request, {})
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
            overall_results = []
            overall_results.append({
                    'result_list': [], 'page': p.screenshot, 'score': 0 ,
                    'no_round': gm.get_round_no(), 'no_successful_round': gm.get_no_rounds_completed(),
                    'no_of_queries_issued_for_current_page': gm.get_no_of_queries_issued_for_current_page(),
                    'no_remaining_rounds': gm.get_remaining_rounds()
            })
            response = render_to_response('rmiyc/game.html', {'overall_results': overall_results}, context)
            response.set_cookie('game_id', game_id)
            # terminate the session whenever the browser closes
            #response.cookies.set_expiry(0)

            return response


def pick_category(request):
        print 'pick category has been called'
        context = RequestContext(request, {})
        scores=[]


        cats = Category

        avatar = GameAvatar('CategoryPage')
        if request.user:
            avatar.update(user=request.user)

        if request.user.is_authenticated():
            postgraduate_score = 0
            undergraduate_score = 0
            research_score = 0
            alumni_score = 0
            student_life_score = 0
            about_glasgow_score = 0
            hs_list = HighScore.objects.filter(user=u)

            for item in hs_list:
                if item.category.name == 'postgraduate':
                    postgraduate_score = item.highest_score
                if item.category.name == 'undergraduate':
                    undergraduate_score = item.highest_score
                if item.category.name == 'research':
                    research_score = item.highest_score
                if item.category.name == 'alumni':
                    alumni_score = item.highest_score
                if item.category.name == 'student_life':
                    student_life_score = item.highest_score
                if item.category.name == 'about_glasgow':
                    about_glasgow_score = item.highest_score
            scores.append({'postgraduate': postgraduate_score, 'undergraduate': undergraduate_score, 'research': research_score,
                       'about_glasgow': about_glasgow_score, 'alumni': alumni_score, 'student_life': student_life_score})
        else:
            scores.append({'postgraduate': 0, 'undergraduate': 0, 'research': 0,
                       'about_glasgow': 0, 'alumni': 0, 'student_life': 0})

        return render_to_response('rmiyc/cat_picker.html', {'scores': scores}, context)


def search(request):

        user = request.user
        result_list = []
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
                    "no_remaining_rounds": gm.get_remaining_rounds()
                }
            else:
                Json_results = {
                    "results": json_objects, "score": s, "is_game_over": 0,
                    "no_round": gm.get_round_no(), "no_successful_round": gm.get_no_rounds_completed(),
                    "no_of_queries_issued_for_current_page": gm.get_no_of_queries_issued_for_current_page(),
                    "no_remaining_rounds": gm.get_remaining_rounds()
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
                           'no_round': gm.get_round_no(), 'no_successful_round': gm.get_no_rounds_completed()})
        response = render_to_response('rmiyc/game_over.html',{'statistics': statistics}, context)
        response.delete_cookie('game_id')
        return response