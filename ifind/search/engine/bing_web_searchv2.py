import json
import string
import requests
import BeautifulSoup as BS
import ifind.search.response as ifind
from ifind.search.searchengine import SearchEngine

# TODO Work out how to generalise the following into perhaps some kind of definition file per engine implementation

API_ENDPOINT = 'https://api.datamarket.azure.com/Bing/Search/v1/'
FORMATS = ["JSON", "ATOM"]
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

DEFAULT_SOURCE_TYPE = WEB_SOURCE_TYPE


class BingWebSearch(SearchEngine):

    def __init__(self, proxy_host=None, api_key=None, **kwargs):

        SearchEngine.__init__(self, proxy_host, api_key, **kwargs)

        self.rootURL = API_ENDPOINT

    def search(self, query):
        """
        Overridden search method for Microsoft's Bing Search

        :param query: ifind.search.query.Query

        :returns ifind.search.response.Response

        :raises urllib2.URLError, API key error

        """

        query_string = self._create_query_string(query)
        results = requests.get(query_string, auth=("", self.api_key))

        if query.format == "ATOM":
            return self._parse_xml_response(query, results)
        if query.format == "JSON":
            return self._parse_json_response(query, results)

        # TODO Exception handling

    def _create_query_string(self, query):
        """

        Generates & returns Bing API query string

        :param query: ifind.search.query.Query
        :return: url string for rest request to bing search api

        """
        if query.source_type in SOURCE_TYPES:
            source_type = query.source_type
        else:
            source_type = DEFAULT_SOURCE_TYPE
            print "*** Warning: Query's source type doesn't match engine's -- See BingWebSearch Class ***"

        if query.format not in FORMATS:
            print "*** Warning: Query's response format doesn't match engine's -- See BingWebSearch Class ***"

        params = {'$format': query.format,
                  '$top': query.top,
                  '$skip': query.skip}

        query_string = '?Query="' + str(query.terms) + '"'

        for key, value in params.iteritems():
            query_string += '&' + key + '=' + str(value)

        return self.rootURL + source_type + self._encode_symbols(query_string)

        # TODO Exception Handling

    def _encode_symbols(self, query_string):
        """
        Encodes query string as defined in the Bing API Specification.

        :param query_string:
        :return encoded_string

        """
        encoded_string = string.replace(query_string, "'", '%27')
        encoded_string = string.replace(encoded_string, '"', '%27')
        encoded_string = string.replace(encoded_string, '+', '%2b')
        encoded_string = string.replace(encoded_string, ' ', '%20')
        encoded_string = string.replace(encoded_string, ':', '%3a')

        return encoded_string

        # TODO Exception Handling

    def _parse_xml_response(self, query, results):
        """
        Parses Bing XML response and returns ifind.search.response.Response object

        :param query: original ifind.search.query.Query object
        :param results: requests response object obtained from API request
        :return: ifind.search.response.Response object

        """

        response = ifind.Response()
        response.query_terms = query.terms

        xmlSoup = BS.BeautifulSoup(results.text)

        for r in xmlSoup.findAll('entry'):
            xmlTitleData = r.find('d:title').string
            xmlURLData = r.find('d:url').string
            xmlDescriptionData = r.find('d:description').string
            response.add_result(xmlTitleData, xmlURLData, xmlDescriptionData)

        return response

        # TODO Exception Handling and further Response refinements

    def _parse_json_response(self, query, results):
        """
        Parses Bing JSON response and returns ifind.seardh.response.Response object

        :param query: original ifind.search.query.Query object
        :param results: requests response object obtained from API request
        :return: ifind.search.response.Response object

        """

        response = ifind.Response()
        response.query_terms = query.terms

        content = json.loads(results.text)

        for r in content[u'd'][u'results']:
            response.add_result(r[u'Title'], r[u'Url'], r[u'Description'])

        return response

        # TODO Exception handling and further Response refinements

        # TODO Wait for further engine implementations before trying to generalise abstract/concrete engine inheritance semantics