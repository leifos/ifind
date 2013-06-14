# -*- coding: utf8 -*-

import urllib


class Query(object):
  """
  OpenSearch Query.
  
  Models an OpenSearch Query element. 
  
  See: http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_Query_element
  
  """
  
  def __init__(self, search_terms):
    """
    Constructor for Query.
    
    Parameters:
    
    * search_terms (str): the search terms of the query
    
    """
    super(Query, self).__init__()
    self.search_terms = search_terms
    self.count = 0
    self.start_index = 0
    self.start_page = 0
    self.language = ''
    self.service = ''
    self.suggestions = {}

    from puppy.query.tokenizer import BasicTokenizer
    self.tokenizer = BasicTokenizer()

  def __eq__(self, q):
      a = self.search_terms
      if isinstance(q, Query):
          b = q.search_terms
      else:
          b = q

      return a == b

  def __hash__(self):
      return hash(self.search_terms)

  def url_quote(self):
      return urllib.quote(self.search_terms)

  def lower(self):
      return Query(self.search_terms.lower())
  
  def __str__(self):
    return self.search_terms

  def tokenize(self):
      return self.tokenizer(self.search_terms)
  
  def write_xml(self):
    """
    Creates XML for OpenSearch Query.
    
    Returns:
    
    * query_xml (str): OpenSearch Query as XML
    
    TODO code Query.write_xml()
    
    """
    pass
  
  
  @staticmethod
  def parse_xml(self, oss_xml):
    """
    Parse OpenSearch Query XML.
    
    Parameters:
    
    * oss_xml (str): OpenSearch Query XML
    
    Returns:
    
    * puppy.model.OpenSearch.Query
    
    TODO code Query.parse_xml()
    
    """
    pass
