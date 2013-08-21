from django.http import HttpResponse
from django.shortcuts import render

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
    query_terms = check_input(request.GET.get('q', ''))

    # bad request
    if not query_terms:
        return HttpResponse(status=400)

    # get exp ID and load experiment
    exp_id = request.session.get('exp_id', False)
    experiment = get_or_create_experiment(exp_id)

    # execute query
    engine = EngineFactory('wikipedia')
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


def IndexView(request):

    # attempt session ID retrieval from user
    exp_id = request.session.get('exp_id', False)
    # attempt exp lookup from ID, creating a new exp otherwise
    experiment = get_or_create_experiment(exp_id)
    # assign new experiment to user
    if not exp_id:
        request.session["exp_id"] = experiment['id']

    template = 'bing.html'

    return render(request, template)


    # generate or get exp
    # exp would say only video and image available