import json
import requests
import oauth2 as oauth
from ifind.search.engine import Engine
from ifind.search.response import Response
from requests.exceptions import ConnectionError

API_ENDPOINT = 'https://api.twitter.com/1.1/search/tweets.json'

KEY_REQUIRED = True # if you count all the nonsense below as a 'key'

CONSUMER_KEY = '1S2HEggPpCnDMmHQMMTt1g'
CONSUMER_SECRET = '3ui76cSSGWB6mUsrB7dL4Pg0fhUqlfNUKfRxZSTrak'

ACCESS_TOKEN_KEY = '330254387-hPlGvv0aCrBwDl2GRyIusgEzWVKryIJwjJU86PLV'
ACCESS_TOKEN_SECRET = '9Zgn25M3QohKCeu65mVtkG1bMun62U2ae5wCv6kys'

OAUTH_TOKEN = oauth.Token(key=ACCESS_TOKEN_KEY, secret=ACCESS_TOKEN_SECRET)    # TODO get api.keys sorted
OAUTH_CONSUMER = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)   # TODO get api.keys sorted

SIGNATURE_METHOD_HMAC_SHA1 = oauth.SignatureMethod_HMAC_SHA1()

RESULT_FORMATS = ("JSON",)

MAX_PAGE_SIZE = 100

MIXED_TYPE = 'mixed'
RECENT_TYPE = 'recent'
POPULAR_TYPE = 'popular'

RESULT_TYPES = (
    MIXED_TYPE,
    RECENT_TYPE,
    POPULAR_TYPE)


class Twitter(Engine):

    def __init__(self, **kwargs):

        """
        Constructor for Twitter engine class, inheriting from ifind's Engine.

        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        Engine.__init__(self, **kwargs)

        if not CONSUMER_KEY or not CONSUMER_SECRET or not ACCESS_TOKEN_KEY or not ACCESS_TOKEN_SECRET:
            raise ValueError('{0} engine OAuth details not supplied'.format(self.name))

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        See: https://dev.twitter.com/docs/api/1.1/get/search/tweets for full list

        Accepted query parameters:

            count:          number of tweets to return per page up to MAX_PAGE_SIZE
            result_type:    'mixed' includes both popular and real time results (default, optional)
                            'recent' returns only the most recent results
                            'popular' returns only the most popular results
            lang:           restricts tweets to given language by ISO 639-1 code, i.e. 'eu' (optional)

        :param query: ifind.search.query.Query object
        :return ifind.search.response.Response object
        :raises Bad request etc

        """

        if not query.top:
            raise ValueError('Total result amount (query.top) not specified'
                             ' in {0} engine search request'.format(self.name))

        if query.top > MAX_PAGE_SIZE:
            raise ValueError('Requested result amount (query.top) exceeds'
                             ' {0} engine max page size'.format(self.name))

        parameters = {'count': query.top,
                      'result_type': query.result_type,
                      'lang': query.lang,
                      'q': query.terms}

        request = oauth.Request.from_consumer_and_token(OAUTH_CONSUMER,
                                                        token=OAUTH_TOKEN,
                                                        http_method='GET',
                                                        http_url=API_ENDPOINT,
                                                        parameters=parameters)

        request.sign_request(SIGNATURE_METHOD_HMAC_SHA1, OAUTH_CONSUMER, OAUTH_TOKEN)

        query_string = request.to_url()

        return Twitter._parse_json_response(query, requests.get(query_string))



    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Bing JSON response and returns ifind.search.response.Response object

        :param query: original ifind.search.query.Query object
        :param results: response object (requests) obtained from API request
        :return: ifind.search.response.Response object

        """
        response = Response()
        response.query_terms = query.terms

        content = json.loads(results.text)

        for result in content[u'statuses']:

            text = result[u'text']
            result_id = str(result[u'id'])
            user_id = result[u'user'][u'id_str']
            created_at = result[u'created_at']

            url = 'https://www.twitter.com/{0}/status/{1}'.format(user_id, result_id)
            title = '{0}'.format(created_at)

            response.add_result(title, url, text)

        return response
