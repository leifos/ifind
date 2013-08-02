from django.http import HttpResponse

from .utils import check_input
from .utils import get_or_create_experiment

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

    # get/create experiment and assign to user if need be
    exp_id = request.session.get('exp_id', False)
    experiment = get_or_create_experiment(exp_id)
    if not exp_id:
        request.session["exp_id"] = experiment['id']

    # execute query
    engine = EngineFactory(experiment['engine'])
    query = Query(query_terms, top=experiment['top'])
    response = engine.search(query)

    return HttpResponse(response.to_json(), content_type='application/json')


def session(request):

    exp_id = request.session.get('exp_id', False)

    if not exp_id:
        return HttpResponse("No experiment assigned, try searching first.")

    experiment = get_or_create_experiment(exp_id)

    engine = experiment['engine']
    top = experiment['top']

    message = "Using experiment '{0}' with '{1}' as engine and '{2}' as max results value.".format(exp_id, engine, top)

    return HttpResponse(message)