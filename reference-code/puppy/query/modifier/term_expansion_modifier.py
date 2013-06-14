# -*- coding: utf8 -*-

from puppy.query import QueryModifier
from puppy.model import Query

class TermExpansionModifier(QueryModifier):
  """
  Expands original query terms with extra terms.

  Parameters:

  * order (int): modifier precedence
  
  * terms (string): the terms to be appended to the query 
  """
  
  def __init__(self, order=0, terms=""):
    super(TermExpansionModifier, self).__init__(order)
    self.description = "Expands original query terms with extra terms."
    self.terms = terms
    
  
  def modify(self, query):
    """Expands query with additional terms.
    
    Parameters:
    
    * query (puppy.model.Query): original query
    
    Returns:
    
    * query (puppy.model.Query): expanded query
    
    """
    query.search_terms = " ".join([query.search_terms, self.terms])
    return query    