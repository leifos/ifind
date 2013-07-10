import requests
import xml.dom.minidom
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.engines.exceptions import EngineException

API_ENDPOINT = 'https://www.wikipedia.org/w/api.php'


class Wikipedia(Engine):
    """
    Wikipedia search engine.

    """

    def __init__(self, **kwargs):
        """
        Wikipedia engine constructor.

        Kwargs:
            See Engine

        Raises:
            CacheException

        Usage:
            See EngineFactory

        """
        Engine.__init__(self, **kwargs)

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.

        Query Args:
            top: specifies maximum amount of results to return, no minimum guarantee

        Returns:
            ifind Response: Object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        Notes:
            See: http://en.wikipedia.org/w/api.php for API documentation.

        """
        if not query.top:
            raise EngineException(self.name, "Total result amount (query.top) not specified")

        return self._request(query)

    def _request(self, query):
        """
        Issues a single request to the API_ENDPOINT and returns the result as
        an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.

        Returns:
            ifind Response: Object encapsulating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
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
        Parses Wikipedia's XML response and returns as an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.
            results : requests library response object containing search results.

        Returns:
            ifind Response: Object encapsulating a search request's results.

        Usage:
            Private Method.

        """
        response = Response(query.terms)

        xml_doc = xml.dom.minidom.parseString(results.content)
        results = xml_doc.getElementsByTagName('Item')

        for result in results:

            title = result.getElementsByTagName('Text')[0].firstChild.data
            url = result.getElementsByTagName('Url')[0].firstChild.data
            summary = result.getElementsByTagName('Description')[0].firstChild.data

            response.add_result(title=title, url=url, summary=summary)

        return response