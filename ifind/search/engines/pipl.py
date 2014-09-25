import json
import requests
import string
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException


API_ENDPOINT = "http://api.pipl.com/search/v3/json/"

DEFAULT_COUNTRY = 'UK'


class Pipl(Engine):
    """
    Pipl search engine.

    """

    def __init__(self, api_key='', **kwargs):
        """
        Pipl engine constructor.

        Kwargs:
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('Pipl api_key='etc123456etc123456etc123456')

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
            http://dev.pipl.com/docs/ for full API documentation.

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

        return Pipl._parse_json_response(query, response)

    def _create_query_string(self, query):
        """
        Creates and returns Pipl API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Pipl API request

        Raises:
            EngineException

        Usage:
            Private method.

        """

        fname = None
        lname = None

        # Assume the query only contains a name at the moment.
        try:
            fname,lname = query.terms.split(' ')
        except ValueError:
            fname = query.terms

        query_append = "?first_name={}&last_name={}&country={}&key={}".format\
            (fname, lname, DEFAULT_COUNTRY, self.api_key)

        print API_ENDPOINT + Pipl._encode_symbols(query_append)
        return API_ENDPOINT + Pipl._encode_symbols(query_append)


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
    def _build_summary(record):
            usernames = []
            try:
                for usr in record[u'usernames']:
                    usernames.append(usr[u'content'])
                usernames = u'\nUsernames: ' + unicode(usernames)
            except:
                usernames = ''

            addresses = []
            try:
                for add in record[u'addresses']:
                    addresses.append(add[u'display'])
                addresses = u'\nAddresses: ' + unicode(addresses)
            except:
                addresses = ''

            relationships = []
            try:
                for rel in record[u'relationships']:
                    relationships.append(rel[u'name'][u'display'])
                relationships = u'\nRelationships: ' + unicode(relationships)
            except:
                relationships = ''

            jobs = []
            try:
                for job in record[u'jobs']:
                    jobs.append(job[u'display'])
                jobs = u'\nJobs: ' + unicode(jobs)
            except:
                job = ''

            educations = []
            try:
                for edu in record[u'educations']:
                    educations.append(edu[u'display'])
                educations = u'\nEducations: ' + unicode(educations)
            except:
                educations = ''

            return "{}{}{}{}{}".format(jobs, addresses, educations, relationships, usernames)


    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Pipl's JSON response and returns as an ifind Response.

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

        for record in content[u'records']:
            name = record[u'names'][0][u'display']
            url = record[u'source'][u'url']
            imageurl = None
            try:
                imageurl = record[u'images'][0][u'url']
            except:
                pass
            summary = Pipl._build_summary(record)

            response.add_result(title=name, url=url, summary=summary, imageurl=imageurl)


        return response

