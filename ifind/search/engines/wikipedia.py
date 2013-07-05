import requests
import xml.dom.minidom
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.engines.exceptions import EngineException

API_ENDPOINT = 'https://www.wikipedia.org/w/api.php'


class Wikipedia(Engine):

    def __init__(self, **kwargs):
        """
        Constructor for Wikipedia engine class, inheriting from ifind's Engine.

        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        Engine.__init__(self, **kwargs)

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        See: http://en.wikipedia.org/w/api.php for API documentation.

        Accepted query parameters:
            top:    specifies maximum amount of results to return, no guarantee on minimum

        :param query: ifind.search.query.Query object
        :return ifind.search.response.Response object
        :raises Bad request etc

        """
        if not query.top:
            raise EngineException(self.name, "Total result amount (query.top) not specified")

        return self._request(query)

    def _request(self, query):

        search_params = {'format': 'xml',
                         'search': query.terms,
                         'action': 'opensearch',
                         'limit': query.top}

        try:
            response = requests.get(API_ENDPOINT, params=search_params)
        except requests.exceptions.ConnectionError:
            raise EngineException(self.name, "Unable to send request, check connectivity")

        if response.status_code != 200:
            raise EngineException(self.name, "", code=response.status_code)

        return Wikipedia._parse_xml_response(query, response)

    @staticmethod
    def _parse_xml_response(query, results):
        """
        Parses Wikipedia XML response and returns ifind.search.response.Response object.

        :param query: original ifind.search.query.Query object
        :param results: response object (requests) obtained from API request
        :return: ifind.search.response.Response object

        """
        response = Response(query.terms)

        xml_doc = xml.dom.minidom.parseString(results.content)
        results = xml_doc.getElementsByTagName('Item')

        for result in results:

            title = result.getElementsByTagName('Text')[0].firstChild.data
            url = result.getElementsByTagName('Url')[0].firstChild.data
            summary = result.getElementsByTagName('Description')[0].firstChild.data

            response.add_result(title, url, summary)

        return response