from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query
from bing_search import run_query
from keys import BING_API_KEY
from ifind.models.game_mechanics import GameMechanic
from ifind.models.game_models import Category
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.

def index(request):

        context = RequestContext(request, {})
        return render_to_response('rmiyc/base.html', context)


def play(request, category_name):
        print 'I have been played'
        '''
            if request.session.test_cookie_worked():
                print "The test cookie worked!!!"
                request.session.delete_test_cookie()
        '''
        # Query the database for the provided category name
        # render the template using the provided context and return as http response.
        user = User.objects.filter(username='testy')
        if user:
            user = user[0]
        else:
            print "Adding testy user"
            user = User(username='testy',password='test')
            user.save()

        c = Category.objects.get(name=category_name)
        gm = GameMechanic()
        if request.COOKIES.has_key('game_id'):

            print 'My game id is ' + request.COOKIES.get('game_id')
            game_id = request.COOKIES.get('game_id')
            gm.retrieve_game(user,game_id)
            gm.take_points()
            gm.set_next_page()
            request.session.set_expiry(0)
        else:
            print 'Im waiting to be assigned to a value'
            gm.create_game(user,c ,0)



        game_id= gm.get_game_id()
        print 'my game_id is:%d ' % (game_id)
        p = gm.get_current_page()

        context = RequestContext(request, {})
        response = render_to_response('rmiyc/game.html', context)
        response.set_cookie('game_id', game_id)
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
        overall_results = []
        result_list = []

        print  'request.method'
        print  request.method
        if request.method == 'post':
            query = request.POST['query'].strip()
            print 'Query'
            print query
            if query:
                result_list = run_query(query)
        else:
            print 'post has not been called'
        overall_results.append(result_list)

        print 'result list'
        print result_list
        print 'overall results'
        print  overall_results
        template = loader.get_template('rmiyc/game.html')
        context = RequestContext(request, {'overall_results': overall_results })
        return HttpResponse(template.render(context))


def game_over(request):
        request.session.set_expiry(datetime.now())
        print 'I am a cookie and I am dying because the game is over'
        context = RequestContext(request, {})
        return render_to_response('rmiyc/cat_picker.html', context)
