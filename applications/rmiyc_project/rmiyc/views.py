from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query
from bing_search import run_query
from keys import BING_API_KEY
from ifind.models.game_mechanics import GameMechanic
from ifind.models.game_models import Category,Page
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.


def index(request):

        context = RequestContext(request, {})
        return render_to_response('rmiyc/base.html', context)


def play(request, category_name):
        print 'I have been played'


        # Adding a dummy user just in the sake of testing
        user = User.objects.filter(username='testy')
        if user:
            user = user[0]
        else:
            print "Adding testy user"
            user = User(username='testy',password='test')
            user.save()

        # Query the database for the provided category name
        c = Category.objects.get(name=category_name)
        gm = GameMechanic()

        # This view shall be called when a new game is to start
        # Thus, there should be no cookie containing a game_id
        if request.COOKIES.has_key('game_id'):
            # redirect the player to the page where they can pick a catefory and start a new game
            response = HttpResponseRedirect('/rmiyc/pick_category/')
            # delete the cookie
            response.delete_cookie('game_id')
            return  response
        else:
            # create a new game
            gm.create_game(user, c, 0)
            # get the game_id to assign it later to a cookie
            game_id = gm.get_game_id()
            # get the current page that is going to be displayed first to the user
            p = gm.get_current_page()
            #
            # get the current score, which I am not sure what it does!!
            s = gm.get_current_score()
            # initiate the array which will hold all the result list, the page that is going to be shown and the score
            overall_results = []
            overall_results.append({'result_list': [], 'page': p.screenshot, 'score': 0})
            context = RequestContext(request, {})
            response = render_to_response('rmiyc/game.html', {'overall_results': overall_results}, context)
            response.set_cookie('game_id', game_id)
            # terminate the session whenever the browser closes
            #response..set_expiry(0)
            return response


def pick_category(request):
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        request.session.set_test_cookie()
        return render_to_response('rmiyc/cat_picker.html', context)


def search(request):
        context = RequestContext(request)
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                print query
                query = Query(query, source_type="Web", format='JSON')
                search_engine = BingWebSearch(api_key=BING_API_KEY)
                result = search_engine.search(query)
                print result

        return render_to_response('rmiyc/search_results.html', { 'result_list': result.results }, context)


def search2(request):

        print 'Search 2 has been called'
         # Adding a dummy user just in the sake of testing
        user = User.objects.filter(username='testy')
        if user:
            user = user[0]
        else:
            print "Adding testy user"
            user = User(username='testy',password='test')
            user.save()

        overall_results = []
        result_list = []
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                result_list = run_query(query)

        if request.COOKIES.has_key('game_id'):
            gm = GameMechanic()
            game_id = request.COOKIES.get('game_id')
            gm.retrieve_game(user,game_id)
            gm.set_next_page()

            p = gm.get_current_page()
            #
            # get the current score, which I am not sure what it does!!
            s = gm.get_current_score()
            overall_results.append({'result_list': result_list, 'page': p.screenshot, 'score': s})
            context = RequestContext(request, {})
            response = render_to_response('rmiyc/game.html', {'overall_results': overall_results}, context)
            return response
        else:
            # the game has not been created yet
            # redirect to play view
            return HttpResponseRedirect('/rmiyc/cat_picker/')


def game_over(request):
        request.session.set_expiry(datetime.now())
        print 'I am a cookie and I am dying because the game is over'
        context = RequestContext(request, {})
        return render_to_response('rmiyc/game_over.html', context)
