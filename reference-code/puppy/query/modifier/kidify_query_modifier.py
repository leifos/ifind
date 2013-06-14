from puppy.lang import Languages
from puppy.core import pmap
from puppy.query.modifier import gs_lookup, KidsModifier
from puppy.model import Query
from puppy.query import ensure_query, QueryModifier

from lxml import etree

from itertools import izip
import urllib2
import urllib


class KidifyQueryModifier(KidsModifier):
    URL = 'http://google.com/complete/search?output=toolbar&q=%s'

    def __init__(self, order=0, modifiers=None):
        """
        
        Construct a KidifyQueryModifier, using your own specified modifier
        terms. Modifier terms are appended to the query to make it more
        oriented to children (e.g., for kids). For the preferred terms, use
        either KidifyQueryModifier.english() or
        KidifyQueryModifier.dutch() to construct a KidifyQueryModifier.
        
        """

        super(KidifyQueryModifier, self).__init__(order=order, modifiers=modifiers)
        self.description = "Modifier terms are appended to the query to make it more oriented to children (e.g., for kids)."

    def for_language(self, language):
        if language == Languages.ENGLISH:
            from puppy.query.modifier.kids_modifier import ENGLISH_MODIFIER_TERMS
            return KidifyQueryModifier(self.order, ENGLISH_MODIFIER_TERMS)
        elif language == Languages.DUTCH:
            from puppy.query.modifier.kids_modifier import DUTCH_MODIFIER_TERMS
            return KidifyQueryModifier(self.order, DUTCH_MODIFIER_TERMS)
        else:
            raise ValueError('language %s not supported' % language)

    def _query_to_ngrams(self, query, num_ngrams):
        """ Turn a query into a set of ngrams from 1 -> num_grams. Returns a
        dict where key = ngram_size and value = list of ngrams """

        terms = query.lower().tokenize()

        ngrams = {}
        for ngram_size in xrange(1, num_ngrams):
            for i in xrange(len(terms) - (ngram_size - 1)):
                ngrams.setdefault(ngram_size, []).append(' '.join(terms[i:i +
                    ngram_size]))

        return ngrams

    def _most_popular_entity_in_query(self, query):
        """ Returns the most popular entity from a query. e.g., "batman is
        cool" -> "batman" """

        ngrams = self._query_to_ngrams(query, 4)

        # lookup all the 1-grams in the GS database. find the most popular in
        # terms of query freqency. this is our most popular entity.

        gs = dict(izip(pmap(gs_lookup, ngrams[1]), ngrams[1]))

        top_score = max(gs.keys())  # top score of the entity
        if top_score is not None:
            # return the entity with the top score
            return gs[top_score]

        # none of the entities were in GS db. Can't do much ...
        return None

    def _query_is_for_kids(self, query):
        best_entity = self._most_popular_entity_in_query(query)
        if best_entity is None:
            # no entity, so we can't make much sense of the query

            return False

        # we found an entity. now let's see if its kid variant is in the GS
        # database.

        return (gs_lookup(super(KidifyQueryModifier, self).modify(best_entity))
                is not None)

    @ensure_query
    def modify(self, query):
        # if we think the query is for kids, just return it. otherwise, kidify
        # it.

        if self._query_is_for_kids(query):
            return query

        return super(KidifyQueryModifier, self).modify(query)


if __name__ == '__main__':
    eng = KidifyQueryModifier().for_language(Languages.ENGLISH)
    q = 'batman is cool'
    assert eng.modify(q) == q
    q = 'genetic tampering'
    assert eng.modify(q) != q

    dut = KidifyQueryModifier().for_language(Languages.DUTCH)
    q = 'voetbal is cool'
    assert dut.modify(q) == q
    q = 'genetic tampering'
    assert dut.modify(q) != q
