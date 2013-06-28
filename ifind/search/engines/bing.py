import json
import string
import requests
import BeautifulSoup as BS
from ifind.search.engine import Engine
from ifind.search.response import Response

# TODO Make definition file. Have constructor for derived classes load it.

API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/Search/v1/'
KEY_REQUIRED = True

FORMATS = ("JSON", "ATOM")

MAX_PAGE_SIZE = 50

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

DEFAULT_SOURCE_TYPE = WEB_SOURCE_TYPE


class Bing(Engine):

    def __init__(self, **kwargs):

        """
        Constructor for BingWebSearch class, inheriting from ifind's SearchEngine.

        :param api_key: string representing unique API access key (optional)
        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        Engine.__init__(self, **kwargs)

        self.root_url = API_ENDPOINT
        self.formats = FORMATS
        self.max_page_size = MAX_PAGE_SIZE
        self.source_types = SOURCE_TYPES

        if (self.api_key is None) and KEY_REQUIRED:
            print 'Key required'
            # TODO raise API KEY Exception

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        N.B. This is derived from ifind's SearchEngine class.

        :param query: ifind.search.query.Query object
        :return ifind.search.response.Response object
        :raises Bad request etc

        """
        query_string = self._create_query_string(query)
        results = requests.get(query_string, auth=("", self.api_key))

        if query.format == 'ATOM':
            return Bing._parse_xml_response(query, results)
        if query.format == 'JSON':
            return Bing._parse_json_response(query, results)

        # TODO Exception handling

    def _create_query_string(self, query):
        """

        Generates & returns Bing API query string

        :param query: ifind.search.query.Query
        :return string representation of query url for REST request to bing search api

        """
        if query.source_type in SOURCE_TYPES:
            source_type = query.source_type
        else:
            source_type = DEFAULT_SOURCE_TYPE
            print "*** Warning: Query source type doesn't match engine's. Using engine default ***"

        if query.format not in FORMATS:
            print "*** Warning: Query source type doesn't match engine's. Using engine default ***"

        # TODO Find a way to define format, top and skip as implementation parameters that need to be matched.
        # TODO Although not too much hassle to just define/adapt/implement here as long as consistent between engines.
        # TODO Maybe have a method called map_query or something that maps the query attributes to what's available.

        params = {'$format': query.format,
                  '$top': query.top,
                  '$skip': query.skip}

        query_string = '?Query="' + str(query.terms) + '"'

        for key, value in params.iteritems():
            query_string += '&' + key + '=' + str(value)

        return self.root_url + source_type + self._encode_symbols(query_string)

        # TODO Exception Handling

    def _encode_symbols(self, query_string):
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

        # TODO Exception Handling

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

        # TODO Exception Handling and further Response refinements

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

        # TODO Exception handling and further Response refinements

        # TODO Further engine implementation needed before generalising abstract/concrete engine inheritance semantics