
from ifind.search.response import Response
from ifind.search.engine import Engine
from ifind.search import Query, EngineFactory
from ifind.search.exceptions import EngineAPIKeyException, QueryParamException, EngineConnectionException
from copy import copy


SM_LIST = ['facebook.com', 'twitter.com', 'plus.google.com', 'uk.linkedin.com', 'bebo.com', 'pinterest.com']


class Socialaccounts(Engine):
    """
    Meta Engine to obtain social media specific results from Bing
    """

    def __init__(self, api_key='',  **kwargs):

        if not api_key:
            raise EngineAPIKeyException(self.name, "Bing API Key Required")

        Engine.__init__(self, **kwargs)
        self.api_key = api_key

    def _search(self, query):
        """

        :param query:

        Query Kwargs:
            site_list (list): A list of sites (social media domain names, preferably) to include in the site: field.
            username (bool): Specify if the search is attempting to list users or not.
        :return:
        """
        responses = []
        sites = query.__dict__.get('site_list', SM_LIST)

        if not query.__dict__.get('username'):
            # It's a general site search, don't supply the intitle field.
            q_base = u"site:{} {}"
        else:
            # Attempt to get user pages by including the intitle field operator.
            q_base = u"site:{} intitle:{}"

        e = EngineFactory('bing', api_key=self.api_key)

        for site in sites:
            terms = q_base.format(site, query.terms)
            # Copy the Query object so the original is not mutated.
            new_query = copy(query)
            new_query.terms = terms

            print new_query.terms
            responses.append(e.search(new_query))

        concat_response = Response(query.terms, query)
        for response in responses:
            for result in response:
                concat_response.add_result_object(result)
        return concat_response