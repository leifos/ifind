from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query

# Create your views here.
def index(request):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/base.html')
        # create and define the context. We don't have any context at the moment
        # but later on we will be putting data in the context which the template engine
        # will use when it renders the template into a page.
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))


def play(request):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/game.html')
        # create and define the context. We don't have any context at the moment
        # but later on we will be putting data in the context which the template engine
        # will use when it renders the template into a page.
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))


def pick_category(request):
        # select the appropriate template to use
        template = loader.get_template('rmiyc/cat_picker.html')
        # create and define the context. We don't have any context at the moment
        # but later on we will be putting data in the context which the template engine
        # will use when it renders the template into a page.
        context = RequestContext(request, {})
        # render the template using the provided context and return as http response.
        return HttpResponse(template.render(context))

def search(request):
        context = RequestContext(request)
        if request.method == 'POST':
            query = request.POST['query'].strip()
            if query:
                query = Query(query, source_type="Web", format='JSON')
                search_engine = BingWebSearch(api_key="")
                result = search_engine.search(query)

        return render_to_response('rmiyc/Game.html',{ 'result_list': result.result_list }, context)