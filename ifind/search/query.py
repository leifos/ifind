class Query(object):
    """
    Models a Query object for use with ifind SearchEngine interface.

    Query Attributes:
        terms:  a string of search terms
        lang:   a string defining the language of the results (varies on engine)
        top:   an integer specifying the number of results to return
        skip:  an integer specifying the offset of starting point for results returned
        result_type: a string defining the type of query (varies on engine)

    """
    def __init__(self, terms, top=10, lang="", result_type=""):
        """
        Constructs Query object, creating instance attributes from optional keyword parameters (**kwargs).

        """
        self.terms = terms
        self.result_type = result_type
        self.lang = lang
        self.top = top
        self.skip = 0

    def __str__(self):
        """
        Returns human-readable string representation of query object.

        """
        return '\n'.join(['{0}: {1}'.format(key, value)
                          for (key, value) in self.__dict__.items()])

    def __eq__(self, other):
        """
        Returns True if both query's attributes are identical, False otherwise.

        """
        return tuple(self.__dict__.items()) == tuple(other.__dict__.items())