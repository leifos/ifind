# -*- coding: utf8 -*-

import string

from puppy.query import QueryFilter
from puppy.model import Query


class BlackListFilter(QueryFilter):
  """
  The BlackList filter looks at the query to check if any terms are contained within the black list if so, they are rejected.

  Parameters:

  * order (int): filter precedence

  * terms: a string containing all the blacklisted terms separated by spaces i.e. ' '
  """
  
  def __init__(self, order=0, terms=""):
    super(BlackListFilter, self).__init__(order)
    self.description = "Rejects queries containing one or more blacklisted words."
    self.terms = set(terms.lower().split())
    
  
  def filter(self, query):
    """Rejects queries containing words in the blacklist.
    
    Parameters:
    
    * query (puppy.model.Query): original query
    
    Returns:
    
    * query (puppy.model.Query): filtered query
    
    """

    original_terms = set(query.search_terms.lower().split())
    return not (original_terms & self.terms)