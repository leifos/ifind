import json
import requests
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException
from ifind.utils.encoding import encode_symbols

API_ENDPOINT = "https://companycheck.co.uk/api/json/"

RESULT_TYPES = ('company', 'director')
DEFAULT_RESULT_TYPE = 'company'


class Companycheck(Engine):
    """
    Companycheck search engine.

    """

    def __init__(self, api_key='', **kwargs):
        """
        Companycheck engine constructor.

        Kwargs:
            See Engine.

        Raises:
            EngineException

        Usage:
            engine = EngineFactory('Companycheck api_key='etc123456etc123456etc123456')

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
          http://help.companycheck.co.uk/hc/en-us/articles/202713993-API-JSON-Documentation for full API documentation.

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

        return Companycheck._parse_json_response(query, response)

    def _create_query_string(self, query):
        """
        Creates and returns Companycheck API query string with encoded query parameters.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            str: query string for Companycheck API request

        Raises:
            EngineException

        Usage:
            Private method.

        """


        if query.result_type:
            result_type = query.result_type
        else:
            result_type = DEFAULT_RESULT_TYPE

        # Check to if the result type is valid
        if result_type not in RESULT_TYPES:
            raise QueryParamException(self.name, "Engine doesn't support query result type '{0}'"
                                                 .format(query.result_type))

        # Build the appropriate query string based on the result type
        if result_type == 'company':
            # Company search format:
            # https://companycheck.co.uk/api/json/ search?name=tesco&apiKey=xxxxxx

            query_append = "search?name={}&apiKey={}".format\
                (query.terms, self.api_key)

        elif result_type == 'director':
            # Director search format:
            # https://companycheck.co.uk/api/json/ directorSearch?name=branson&postcode=W11&apiKey=xxxxxx

            query_append = "directorSearch?name={}&apiKey={}".format\
                (query.terms, self.api_key)
        else:
            raise QueryParamException(self.name, "No handler found for result type: {}"
                                                 .format(query.result_type))

        return API_ENDPOINT + encode_symbols(query_append)

    @staticmethod
    def _build_company_summary(company):
        """
        Builds the summary portion of the company result

        :param: dict - company - company dictionary from the companycheck JSON response
        :return: str - summary
        """
        country = u'Country: ' + company[u'country']
        address = u'\nAddress: ' + company[u'address']
        sic = u'\nSic code: ' +  company[u'sic']
        status = u'\nStatus: ' + company[u'status']

        return country + address + sic + status

    @staticmethod
    def _build_director_summary(director):
        """
        Builds the summary portion of the directors result

        :param: dict - company - company dictionary from the companycheck JSON response
        :return: str - summary
        """
        postcodes = []
        for pcode in director[u'registeredPostcodes']:
            postcodes.append(unicode(pcode[u'postcode0']))
        postcodes = u'Registered Postcodes: ' + unicode(postcodes)

        return postcodes

    @staticmethod
    def _parse_json_response(query, results):
        """
        Parses Companycheck's JSON response and returns as an ifind Response.

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
        url_base = 'http://companycheck.co.uk/'


        if query.result_type:
            result_type = query.result_type
        else:
            result_type = DEFAULT_RESULT_TYPE


        if result_type == 'company':
            for company in content:
                name = company[u'name']
                url =  url_base + 'company/' + str(company[u'number'])
                imageurl = None
                summary = Companycheck._build_company_summary(company)
                response.add_result(title=name, url=url, summary=summary, imageurl=imageurl)

        elif result_type == 'director':
            for director in content:
                name = director[u'name']
                url =  url_base + 'director/' + str(director[u'number'])
                imageurl = None
                summary = Companycheck._build_director_summary(director)
                response.add_result(title=name, url=url, summary=summary, imageurl=imageurl)

        return response

