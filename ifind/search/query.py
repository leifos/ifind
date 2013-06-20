class Query(object):
    """
    Models a Query object for use with SearchEngine interface.

    """

    def __init__(self, terms, **kwargs):
        """
        Constructs Query object, taking optional keyword parameters as instance attributes.

        :param self:
        :param terms: the search terms of the query (str)

        """
        self.terms = terms

        for key, value in kwargs.items():
            setattr(self, key, value)

    #TODO Do we let punctuation ruin an otherwise perfectly equal couple of queries? Do we strip 'em?
    def __eq__(self, other):
        return set(self.terms.lower()) == set(other.terms.lower())

    def __str__(self):
        return "Search Terms: {0}".format(self.terms)