import json
import requests
import string
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException


API_ENDPOINT = "https://www.googleapis.com/plus/v1/"

RESULT_TYPES = ('people', 'activities')
DEFAULT_RESULT_TYPE = 'activities'
MAX_PAGE_SIZE = {'people': 50, 'activities': 20}

class Googleplus(Engine):
    """
    Googleplus search engine.

    """

    def __init__(self, api_key='', **kwargs):
        """
        Googleplus engine constructor.

        Kwargs:
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('Googleplus api_key='etc123456etc123456etc123456')

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
            top (int): number of tweets to return up to MAX_PAGE_SIZE
        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        Notes:
            https://developers.google.com/ for full API documentation.

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

        return Googleplus._parse_json_response(query, response)

    def _create_query_string(self, query):
        """
        Creates and returns Googleplus API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Googleplus API request

        Raises:
            EngineException

        Usage:
            Private method.

        """

        # Set the result type
        if query.result_type:
            result_type = query.result_type

        else:
            result_type = DEFAULT_RESULT_TYPE

        # Check to if the result type is valid
        if result_type not in RESULT_TYPES:
            raise QueryParamException(self.name, "Engine doesn't support query result type '{0}'"
                                                 .format(query.result_type))

        # Set the number of results to get back, max value specified at the top of this file
        if query.top and query.top <= MAX_PAGE_SIZE[result_type]:
            top = query.top
        else:
            top = MAX_PAGE_SIZE[result_type]

        # Dictionary of search paramaters
        search_params = {'result_type': result_type,
                         'q': query.terms,
                         'top': top,
                         }
        # Craft the string to append to the endpoint url
        query_append = "{}?query='{}'&maxResults={}&key={}".format\
            (search_params['result_type'], search_params['q'], search_params['top'] , self.api_key)

        return API_ENDPOINT + Googleplus._encode_symbols(query_append)


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
    def _resize_image(imageurl, newsize=125):
        """

        :param imageurl: The Googleplus image url
        :param newsize:  The new size of the url, the API returns ?sz=50
        :return: Returns the new URL with the size update
        """
        return imageurl.split('?sz=')[0] + '?sz=' + str(newsize)

    @staticmethod
    def _build_activity_summary(activity):
        object = "\n" + activity[u'object'][u'objectType'] + "\n" + activity[u'object'][u'content']
        attachment =''

        try:
            activity[u'object'][u'attachments']
            attachment = "\nAttachment: "
        except KeyError:
            pass

        if attachment:
            attachment += activity[u'object'][u'attachments'][0][u'objectType']
            try:
                attachment += activity[u'object'][u'attachments'][0][u'displayName']
            except KeyError:
                pass
            attachment += "\n" + activity[u'object'][u'attachments'][0][u'url']

        actorname = activity[u'actor'][u'displayName']
        published = activity[u'published']
        summary = u"User: {}\nPublished: {}{}{}".format(actorname, published, object, attachment)

        return summary

    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Googleplus's JSON response and returns as an ifind Response.

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

        result_type = DEFAULT_RESULT_TYPE
        if query.result_type:
            result_type = query.result_type

        if result_type == 'people':
            for user in content[u'items']:
                name = user[u'displayName']
                url = user[u'url']
                imageurl = Googleplus._resize_image(user[u'image'][u'url'])
                summary = ''
                response.add_result(title=name, url=url, summary=summary, imageurl=imageurl)

        elif result_type == 'activities':
            for activity in content[u'items']:
                title = activity[u'verb'] + ' '  +  activity[u'title']
                url = activity[u'url']
                summary = Googleplus._build_activity_summary(activity)
                imageurl = ''
                try:
                    imageurl = activity[u'image'][u'url']
                except KeyError:
                    pass
                response.add_result(title=title, url=url, summary=summary, imageurl=imageurl)

        return response

