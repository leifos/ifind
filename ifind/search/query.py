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
        """
        Equality method.

        """
        return set(self.terms.lower()) == set(other.terms.lower())

    def __str__(self):
        """
        Returns human-readable string representation of query object.
        """
        return '\n'.join(['{0}: {1}'.format(key, value) for (key, value) in self.__dict__.items()])