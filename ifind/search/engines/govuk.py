import requests
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.engines.exceptions import EngineException

API_ENDPOINT = 'https://www.gov.uk/api/search.json?q=court+claim+for+money'


class GovUK(Engine):

    def __init__(self, **kwargs):

        Engine.__init__(self, **kwargs)

    def _search(self, query):

        if not query.top:
            raise EngineException(self.name, "Total result amount (query.top) not specified")

        return self._request(query)

    def _request(self, query):

        search_params = {'q': query.terms}

        try:
            response = requests.get(API_ENDPOINT, params=search_params)
        except requests.exceptions.ConnectionError:
            raise EngineException(self.name, "Unable to send request, check connectivity")

        import pprint
        pprint.pprint(response.content)


        return GovUK._parse_json_response(query, response)