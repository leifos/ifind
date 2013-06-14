# -*- coding: utf8 -*-

from puppy.query import QueryFilter
from puppy.model import Query

class TestError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return "Error comparing term list "+repr(self.value)


class TestEqualFilter(QueryFilter):
  """Similar to an assert, compares the search terms with terms in a list."""
  
  def __init__(self, order=0, terms=""):
    super(TestEqualFilter, self).__init__(order)
    self.description = "Compare the search terms with terms in a list, for debugging."
    self.terms = terms
    
  
  def run(self, query):
    """Compare the search terms.
    
    Parameters:
    
    * query (puppy.model.Query): original query
    
    Returns:
    
    * query (puppy.model.Query): original query or exception if both sets are different
    
    """
    original_terms = set(query.search_terms.lower().split())
    extra_terms = set(self.terms.lower().split())
    difference =  original_terms.symmetric_difference(extra_terms)
    if len(difference):
      raise TestError(difference)
    return query
    
