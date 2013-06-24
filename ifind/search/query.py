class Query(object):
    """
    Models a Query object for use with SearchEngine interface.

    Query Attributes:
        terms: a string of search terms (str)
        lang:  a string defining the language of the query/response (str)
        top:   an integer specifying the number of results to return (int)
        skip:  an integer specifying the offset for the starting point of results returned (int)
    """
    def __init__(self, terms, source_type=None, **kwargs):
        """
        Constructs Query object, taking optional keyword parameters as instance attributes.

        :param self:
        :param terms: the search terms of the query (str)
        :param source_type: data type of search response

        """
        self.terms = terms
        self.source_type = source_type
        self.format = 'ATOM'
        self.lang = 'EN'
        self.top = 10
        self.skip = 0

        for key, value in kwargs.items():
            setattr(self, key, value)

    # TODO: Use query_hash here to resolve equality.
    def __eq__(self, other):
        """
        Equality method.

        """
        return set(self.terms.lower()) == set(other.terms.lower())

    def __str__(self):
        """
        Returns human-readable string representation of query object.
        """
        return '\n'.join(['{0}: {1}'.format(key, value) for (key, value) in self.__dict__.items()])

    def query_hash(self):
        """
        Hashes the attributes of the query
        :return: a hash string of the query

        """
        # TODO: Use query attributes for hashing
        pass

