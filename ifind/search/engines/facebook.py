import json
import requests
import string
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException


API_ENDPOINT = "https://graph.facebook.com/v2.1/"

RESULT_TYPES = ('user', 'page', 'location', 'group', 'place')
DEFAULT_RESULT_TYPE = 'user'

class Facebook(Engine):
    """
    Facebook search engine.

    """

    def __init__(self, api_key='', **kwargs):
        """
        Facebook engine constructor.

        Kwargs:
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('Facebook api_key='etc123456etc123456etc123456')

        """
        Engine.__init__(self, **kwargs)
        self.api_key = api_key

        if not self.api_key:
            raise EngineAPIKeyException(self.name, "'api_key=' keyword argument not specified")

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.

        Query Kwargs:
            result_type (str): specifies the type of results to return (see top of class for available types).

        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        Notes:
            https://developers.facebook.com/docs for full API documentation.

        """
        return self._request(query)

    def _request(self, query):
        """
        Issues a single request to the API_ENDPOINT and returns the result as
        an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        query_string = self._create_query_string(query)

        try:
            response = requests.get(query_string)
        except requests.exceptions.ConnectionError:

            raise EngineConnectionException(self.name, "Unable to send request, check connectivity.")

        if response.status_code != 200:
            raise EngineConnectionException(self.name, "", code=response.status_code)

        return Facebook._parse_json_response(query, response)

    def _create_query_string(self, query):
        """
        Creates and returns Facebook API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Facebook API request

        Raises:
            EngineException

        Usage:
            Private method.

        """

        result_type = query.result_type
        if not result_type:
            result_type = DEFAULT_RESULT_TYPE

        if result_type not in RESULT_TYPES:
            raise QueryParamException(self.name, "Engine doesn't support query result type '{0}'"
                                                 .format(query.result_type))

        search_params = {'result_type': result_type,
                         'q': query.terms}

        query_append = "search?q={}&type={}&access_token={}".format\
            (search_params['q'], search_params['result_type'], self.api_key)

        return API_ENDPOINT + Facebook._encode_symbols(query_append)


    @staticmethod
    def _encode_symbols(query_string):
        """
        Encodes symbols for http get.

        Args:
            query_string (str): query string for Bing API request.

        Returns:
            str: encoded query string for Bing API request.

        Usage:
            Private method.

        """
        encoded_string = string.replace(query_string, "'", '%27')
        encoded_string = string.replace(encoded_string, '"', '%27')
        encoded_string = string.replace(encoded_string, '+', '%2b')
        encoded_string = string.replace(encoded_string, ' ', '%20')
        encoded_string = string.replace(encoded_string, ':', '%3a')

        return encoded_string

    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Facebook's JSON response and returns as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.
            results : requests library response object containing search results.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Usage:
            Private method.


        """

        response = Response(query.terms)
        content = json.loads(results.text)

        if query.result_type == 'user' or not query.result_type:
            # Sample response
            #     {
            # "data": [
            #   {
            #      "name": "John Doe",
            #      "id": "999999999999999"
            #   },
            #   {
            #      "name": "John Doe",
            #      "id": "88888888888888"
            #   }
            #   ],
            #        "paging": {
            #           "next": "long_url"
            #        }
            #     }

            # The base URL is used to create the link to the profile, it will redirect to a permanent user URL.
            base_url= "https://www.facebook.com/app_scoped_user_id/"
            for user in content[u'data']:
                name = user[u'name']
                tempid = user[u'id']
                url = base_url + tempid + '/'
                text = ''
                # Minimal information, probably need a second round of querying the API for each user to get something
                # for the snippet. Better way?
                response.add_result(title=name, url=url, summary=text)

            # Implement the other search tpyes.

        return response