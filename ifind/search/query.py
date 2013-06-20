__author__ = 'leifos'


class Query(object):
    """
    Models a Query object for use with SearchEngine interface.

    Query Attributes:
        search_terms: a string of search terms
        lang: a string defining the language of the query/response
        page: an integer specifying what page of results to return
        results_per_page: (integer) the desired number of results per page
    """

    def __init__(self, terms, **kwargs):
        """
        Constructs Query object, taking optional keyword parameters as instance attributes.

        :param self:
        :param terms: the search terms of the query (str)

        """
        self.terms = terms
        self.lang = 'EN'
        self.page = 1
        self.results_per_page = 10

        for key, value in kwargs.items():
            setattr(self, key, value)

    #TODO Do we let punctuation ruin an otherwise perfectly equal couple of queries? Do we strip 'em?
    def __eq__(self, other):
        return set(self.terms.lower()) == set(other.terms.lower())

    def __str__(self):
        return "Search Terms: {0}".format(self.terms)


    def query_hash(self):
        """
        hashes the attributes of the query
        :return: a hash string of the query

        """
        pass
