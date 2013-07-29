from django.http import HttpResponse

from .utils import check_input

from ifind.search import Query
from ifind.search import EngineFactory


def search(request):
    """
    Accepts GET request containing query terms,
    searches and returns results as JSON.

    """
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
    query = Query(query_terms, top=50)
    response = engine.search(query)

    return HttpResponse(response.to_json(), content_type='application/json')



