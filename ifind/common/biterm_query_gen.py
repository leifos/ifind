"""
A class which inherits from QueryGeneration to generate queries list of biterms
Might be better moving the extract queries methods from single term generation
into the superclass, then can inherit from that and just do the bit
where you generate all combinations of two terms
This would be more extensible as could rename this class multiterm
Just set the number of terms, and adapt the combination method to
combine into groups of numTerms
Not sure I'm getting inheritance quite right in Python.. need to look at this
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
from query_generation import QueryGeneration
from single_term_query_gen import SingleTermQueryGeneration
from itertools import combinations

class BiTermQueryGeneration(QueryGeneration):
    """
    Implementation of QueryGeneration which generates single term queries
    """
    _single_generator = QueryGeneration

    def __init__(self):
        _singleGenerator = SingleTermQueryGeneration()

    def extract_queries_from_html(self, html):
        """
        uses a single generator to generate a list of
        single terms, then uses combine method to generate all
        possible pairs
        :param html:
        :return:
        """
        singleTerms = self._single_generator._extract_queries_from_html(html)
        return self.combine(singleTerms)

    def extract_queries_from_text(self, text):
        singleTerms = self._single_generator._extractQueriesFromText(text)
        return self.combine(singleTerms)

    #todo (rose) update method to use nltk
    def combine(self, singleTerms):
        #returns a list of tuples of length two
        #contains all unique combos of single terms length 2
        length = 2
        pairs = list(combinations(singleTerms,length))
        doubles = [] # create an empty list to hold the strings of pairs
        for pair in pairs:
            combined = pair[0] + " " + pair[1]
            doubles.append(combined)

        return doubles



