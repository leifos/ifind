import json
import string
import requests
import BeautifulSoup as BS
from ifind.search.engine import Engine
from ifind.search.response import Response
from requests.exceptions import ConnectionError

API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/Search/v1/'

RESULT_FORMATS = ("JSON", "ATOM")

MAX_PAGE_SIZE = 50
MAX_RESULTS = 1000

WEB_RESULT_TYPE = 'Web'
IMAGE_RESULT_TYPE = 'Image'
VIDEO_RESULT_TYPE = 'Video'
NEWS_RESULT_TYPE = 'News'
SPELL_RESULT_TYPE = 'Spell'

RESULT_TYPES = (
    WEB_RESULT_TYPE,
    IMAGE_RESULT_TYPE,
    NEWS_RESULT_TYPE,
    SPELL_RESULT_TYPE)


class Bing(Engine):

    def __init__(self, api_key='', **kwargs):

        """
        Constructor for Bing engine class, inheriting from ifind's Engine.

        :param api_key: string representing unique API access key
        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        Engine.__init__(self, **kwargs)
        self.api_key = api_key

        if not self.api_key:
            raise ValueError("{0} engine 'api_key' keyword argument not specified".format(self.name))

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        See: ifind's dropbox for recent Bing API specification for full list

        Accepted query parameters:
            top:            specifies the number of results to return up to MAX_PAGE_SIZE
            skip:           specifies the offset requested for the starting point of results returned
            format:         specifies the result format i.e. 'atom' or 'json'
            result_type:    specifies the type of query (see top of Bing source for available types)


        :param query: ifind.search.query.Query object
        :return ifind.search.response.Response object
        :raises Bad request etc

        """
        if query.top <= MAX_PAGE_SIZE:
            return self._request(query)

        if query.top > MAX_PAGE_SIZE:
            return self._auto_request(query)

    def _request(self, query):

        query_string = self._create_query_string(query)

        try:
            results = requests.get(query_string, auth=('', self.api_key))
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Internet connectivity error with {0} engine search request".format(self.name))

        if results.status_code == 401:
            raise ValueError("Incorrect API Key supplied to {0} engine search request (401)".format(self.name))
        if results.status_code == 400:
            raise ValueError("Bad request sent to {0} engine search request API (400)".format(self.name))

        if query.format == 'ATOM':
            return Bing._parse_xml_response(query, results)
        if query.format == 'JSON':
            return Bing._parse_json_response(query, results)

    def _auto_request(self, query):

        target = query.top
        query.top = MAX_PAGE_SIZE
        query.skip = 0
        response = self._request(query)

        while response.result_total < target:

            remaining = target - response.result_total

            if remaining > MAX_PAGE_SIZE:
                query.skip += MAX_PAGE_SIZE
                query.top = MAX_PAGE_SIZE
                response += self._request(query)

            if remaining <= MAX_PAGE_SIZE:
                query.skip += query.top
                query.top = remaining
                response += self._request(query)

        return response

    def _create_query_string(self, query):
        """

        Generates & returns Bing API query string

        :param query: ifind.search.query.Query
        :return string representation of query url for REST request to bing search api

        """
        if not query.top:
            raise ValueError("Total result amount (query.top) not specified"
                             " in {0} engine search request".format(self.name))

        if query.top > MAX_RESULTS:
            raise ValueError("Total result amount (query.top) exceeds"
                             " {0} engine result limit".format(self.name))

        if query.result_type.title() not in RESULT_TYPES:
            raise ValueError("{0} engine doesn't support '{1}' result_type for query".format(self.name, query.result_type))

        if query.format not in RESULT_FORMATS:
            raise ValueError("{0} engine doesn't support '{1}' result format for query".format(self.name, query.format))

        params = {'$format': query.format,
                  '$top': query.top,
                  '$skip': query.skip}

        query_string = '?Query="' + str(query.terms) + '"'

        for key, value in params.iteritems():
            query_string += '&' + key + '=' + str(value)

        return API_ENDPOINT + query.result_type + Bing._encode_symbols(query_string)

    @staticmethod
    def _parse_xml_response(query, results):
        """
        Parses Bing XML response and returns ifind.search.response.Response object

        :param query: original ifind.search.query.Query object
        :param results: response object (requests) obtained from API request
        :return: ifind.search.response.Response object

        """
        response = Response()
        response.query_terms = query.terms

        xmlSoup = BS.BeautifulSoup(results.text)

        for result in xmlSoup.findAll('entry'):
            title = result.find('d:title').string
            url = result.find('d:url').string
            description = result.find('d:description').string
            response.add_result(title, url, description)

        return response

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

        for result in content[u'd'][u'results']:
            response.add_result(result[u'Title'], result[u'Url'], result[u'Description'])

        return response

    @staticmethod
    def _encode_symbols(query_string):
        """
        Encodes query string as defined in the Bing API Specification.

        :param query_string: string representation of query url for REST request to bing search api
        :return encoded query string

        """
        encoded_string = string.replace(query_string, "'", '%27')
        encoded_string = string.replace(encoded_string, '"', '%27')
        encoded_string = string.replace(encoded_string, '+', '%2b')
        encoded_string = string.replace(encoded_string, ' ', '%20')
        encoded_string = string.replace(encoded_string, ':', '%3a')

        return encoded_string