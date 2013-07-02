import json
import string
import requests
import BeautifulSoup as BS
from ifind.search.engine import Engine
from ifind.search.response import Response

API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/Search/v1/'
KEY_REQUIRED = True

RESULT_FORMATS = ("JSON", "ATOM")

MAX_PAGE_SIZE = 50
MAX_RESULTS = 1000

WEB_SOURCE_TYPE = 'Web'
IMAGE_SOURCE_TYPE = 'Image'
VIDEO_SOURCE_TYPE = 'Video'
NEWS_SOURCE_TYPE = 'News'
SPELL_SOURCE_TYPE = 'Spell'

SOURCE_TYPES = (
    WEB_SOURCE_TYPE,
    IMAGE_SOURCE_TYPE,
    NEWS_SOURCE_TYPE,
    SPELL_SOURCE_TYPE
)


class Bing(Engine):

    def __init__(self, **kwargs):

        """
        Constructor for BingWebSearch class, inheriting from ifind's SearchEngine.

        :param api_key: string representing unique API access key (optional)
        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        Engine.__init__(self, **kwargs)

        if not self.api_key and KEY_REQUIRED:
            raise ValueError('{0} engine API Key not supplied'.format(self.name))

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        N.B. This is derived from ifind's SearchEngine class.

        :param query: ifind.search.query.Query object
        :return ifind.search.response.Response object
        :raises Bad request etc

        """
        #
        # auto query
        #
        
        if query.top <= MAX_PAGE_SIZE:
            return self._issue_request(query)

        # if query.top <= MAX_PAGE_SIZE:
            # create query string with query
            # make query request
            # parse and return
              
        # if query.top > MAX_PAGE_SIZE:
        #     target = query.top
        #     query.top = MAX_PAGE_SIZE
        #     # issue initial request, get response
        #     while response.result_total < target:
        #
        #         if (target-response.result_total) > MAX_PAGE_SIZE:
        #             query.skip += MAX_PAGE_SIZE
        #             query.top = MAX_PAGE_SIZE
        #             # issue request, get response add returned response to current with '+=' operator
        #
        #
        #         if (target-response.result_total) < MAX_PAGE_SIZE:
        #             query.skip += query.top
        #             query.top = target-response.result_total
        #             # issue request, get response add returned response to current with '+=' operator
        #
        # TODO: Flow controls, test response '+=' addition (probably did already), test this. Maybe with tests.



    def _issue_request(self, query):

        query_string = self._create_query_string(query)

        try:
            results = requests.get(query_string, auth=('', self.api_key))
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("Internet connectivity error")

        if results.status_code == 401:
            raise ValueError("Incorrect API Key supplied to {0} engine (401)".format(self.name))
        if results.status_code == 400:
            raise ValueError("Bad request sent to {0} engine API (400)".format(self.name))

        if query.format == 'ATOM':
            return Bing._parse_xml_response(query, results)
        if query.format == 'JSON':
            return Bing._parse_json_response(query, results)

    def _create_query_string(self, query):
        """

        Generates & returns Bing API query string

        :param query: ifind.search.query.Query
        :return string representation of query url for REST request to bing search api

        """
        if query.source_type.title() not in SOURCE_TYPES:
            raise ValueError("{0} engine doesn't support '{1}' source type".format(self.name, query.source_type))

        if query.format not in RESULT_FORMATS:
            raise ValueError("{0} engine doesn't support '{1}' result format".format(self.name, query.format))

        #if query.

        # TODO Create method map_query that adjusts params to match bing spec/def
        # TODO The above source/format checks would happen in map query

        params = {'$format': query.format,
                  '$top': query.top,
                  '$skip': query.skip}

        query_string = '?Query="' + str(query.terms) + '"'

        for key, value in params.iteritems():
            query_string += '&' + key + '=' + str(value)

        return API_ENDPOINT + query.source_type + Bing._encode_symbols(query_string)

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
