from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query
from bing_search import run_query


# Create your views here.
def index(request):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/base.html')
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))


def play(request, category_name):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/game.html')
        # Query the database for the provided category name

        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))


def pick_category(request):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/cat_picker.html')
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))


def search(request):
        context = RequestContext(request)
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                print query
                query = Query(query, source_type="Web", format='JSON')
                search_engine = BingWebSearch(api_key="m8KBb9SgQxAAnoAl6PJRnCqdaaKQKVk3Z+iWnj4OR5s")
                result = search_engine.search(query)
                print result


        return render_to_response('rmiyc/Game.html',{ 'result_list': result.results }, context)


def search2(request):
        context = RequestContext(request)
        result_list = []
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                result_list = run_query(query)

        return render_to_response('rmiyc/Game.html',{ 'result_list': result_list }, context)