class Query(object):
    """
    Models a Query object for use with ifind's searching interface.

    """
    def __init__(self, terms, top=10, lang="", result_type=""):
        """
        Query constructor.

        Args:
            terms (str): Search terms.

        Kwargs:
            top (int): maximum number of results to return
            lang (str): preferred language of returned results (engine specific)
            result_type (str): type of query (engine specific)

        Attributes:
            skip (int): offset of starting point for results returned

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
        Returns True if both querys hash to the same value, False otherwise.

        """
        return hash(self) == hash(other)

    def __hash__(self):
        """
        Returns hash of tupled instance attributes of query.

        """
        return hash(tuple(self.__dict__.items()))