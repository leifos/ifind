from django.views.generic.list import ListView
from django.http import HttpResponse

from ifind.search import Query
from ifind.search import EngineFactory


class ResultListView(ListView):
    """
    Generic view to render a list of search results.

    """
    template_name = 'index.html'
    context_object_name = 'result_list'

    def get_queryset(self):

        engine = EngineFactory('govuk')
        query = Query(self.request.REQUEST['q'], top=10)

        return engine.search(query).results



