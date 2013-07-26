import json
import string

from django.views.generic.list import ListView
from django.http import HttpResponse

from .utils import check_input

from ifind.search import Query
from ifind.search import EngineFactory

#
# class ResultListView(ListView):
#     """
#     Generic view to render a list of search results.
#
#     """
#     template_name = 'index.html'
#     context_object_name = 'result_list'
#
#     def get_queryset(self):
#
#         engine = EngineFactory('govuk')
#         query = Query(self.request.REQUEST['q'], top=10)
#
#         return engine.search(query).results


def search(request):

    # invalid HTTP method
    if request.method != 'GET':
        return HttpResponse(status=405)

    # checks input for validity
    query_terms = check_input(request.GET.get('q', ""))

    # bad request
    if not query_terms:
        return HttpResponse(status=400)

    # execute query
    engine = EngineFactory('govuk')
    query = Query(query_terms)
    response = engine.search(query)

    return HttpResponse(response.to_json(), content_type='application/json')



