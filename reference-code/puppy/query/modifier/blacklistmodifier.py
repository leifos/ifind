# -*- coding: utf8 -*-

from puppy.query import QueryModifier
from puppy.model import Query

class BlackListModifier(QueryModifier):
    """
    Expands original query terms with extra terms.

    Parameters:

    * terms (string): the terms to be appended to the query
    """

    def __init__(self, order=0, terms="", null_query="games"):
        super(BlackListModifier, self).__init__(order)
        self.description = "Removes specified terms occurring in the original query"
        self.termlist = terms.split(' ')
        self.null_query = null_query


    def modify(self, query):
        """Removes the specified terms that appear in the query - ie. removes blacklisted terms.
        if this results in a null query, then the null_query is used.

        Parameters:

        * query (puppy.model.Query): original query

        Returns:

        * query (puppy.model.Query): contracted query, or null_query

        """
        print "Query before Blacklisting: " + query.search_terms
        q = ''

        for t in query.search_terms.split(' '):
            if t in self.termlist:
                pass
            else:
                q = q + ' ' + t
        # if all the terms in the query are on the black list then assign the null query

        if q:
            pass
        else:
            q = self.null_query

        print "Query after Blacklisting: " + q

        query.search_terms = q

        return query
