import json
import requests
import oauth2 as oauth
from ifind.search.engine import Engine
from ifind.search.response import Response
from engines.exceptions import EngineException

API_ENDPOINT = 'https://api.twitter.com/1.1/search/tweets.json'

CONSUMER_KEY = '1S2HEggPpCnDMmHQMMTt1g'
CONSUMER_SECRET = '3ui76cSSGWB6mUsrB7dL4Pg0fhUqlfNUKfRxZSTrak'

ACCESS_TOKEN_KEY = '330254387-hPlGvv0aCrBwDl2GRyIusgEzWVKryIJwjJU86PLV'
ACCESS_TOKEN_SECRET = '9Zgn25M3QohKCeu65mVtkG1bMun62U2ae5wCv6kys'

OAUTH_TOKEN = oauth.Token(key=ACCESS_TOKEN_KEY, secret=ACCESS_TOKEN_SECRET)    # TODO get api.keys sorted
OAUTH_CONSUMER = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)   # TODO get api.keys sorted

SIGNATURE_METHOD_HMAC_SHA1 = oauth.SignatureMethod_HMAC_SHA1()

RESULT_TYPES = ('mixed', 'recent', 'popular')

DEFAULT_RESULT_TYPE = 'mixed'

MAX_PAGE_SIZE = 100


class Twitter(Engine):
    """
    Bing search engine.

    """

    def __init__(self, **kwargs):
        """
        Twitter engine constructor.

        Kwargs:
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('twitter')

        """
        Engine.__init__(self, **kwargs)

        if not CONSUMER_KEY or not CONSUMER_SECRET or not ACCESS_TOKEN_KEY or not ACCESS_TOKEN_SECRET:
            raise EngineException(self.name, 'OAuth details not supplied')

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): Object encapsulating details of a search query.

        Query Kwargs:
            top (int): number of tweets to return up to MAX_PAGE_SIZE
            result_type (str): 'mixed' - popular and recent results
                               'recent' - most recent results
                               'popular' - most popular results
            lang (str): restricts tweets to given language by ISO 639-1 code, i.e. 'eu'

        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        Notes:
            https://dev.twitter.com/docs/api/1.1/get/search/tweets for full API documentation.

        """
        if not query.top:
            raise EngineException(self.name, "Total result amount (query.top) not specified")

        if query.top > MAX_PAGE_SIZE:
            raise EngineException(self.name, 'Requested result amount (query.top) '
                                             'exceeds max of {0}'.format(MAX_PAGE_SIZE))
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
            raise EngineException(self.name, "Unable to send request, check connectivity")

        if response.status_code != 200:
            raise EngineException(self.name, "", code=response.status_code)

        return Twitter._parse_json_response(query, response)

    def _create_query_string(self, query):
        """
        Creates and returns Twitter API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Twitter API request

        Raises:
            EngineException

        Usage:
            Private method.

        """
        if not query.result_type:
            query.result_type = DEFAULT_RESULT_TYPE

        if query.result_type not in RESULT_TYPES:
            raise EngineException(self.name, "Engine doesn't support query result type '{0}'".format(query.result_type))

        search_params = {'count': query.top,
                         'result_type': query.result_type,
                         'lang': query.lang,
                         'q': query.terms}

        request = oauth.Request.from_consumer_and_token(OAUTH_CONSUMER,
                                                        token=OAUTH_TOKEN,
                                                        http_method='GET',
                                                        http_url=API_ENDPOINT,
                                                        parameters=search_params)

        request.sign_request(SIGNATURE_METHOD_HMAC_SHA1, OAUTH_CONSUMER, OAUTH_TOKEN)

        return request.to_url()

    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Twitter's JSON response and returns as an ifind Response.

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

        for result in content[u'statuses']:

            text = result[u'text']
            result_id = str(result[u'id'])
            user_id = result[u'user'][u'id_str']
            created_at = result[u'created_at']
            url = 'https://www.twitter.com/{0}/status/{1}'.format(user_id, result_id)

            response.add_result(title=created_at, url=url, summary=text)

            if len(response) == query.top:
                break

        return response