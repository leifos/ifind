# -*- coding: utf8 -*-
from puppy.core.type_checking import check
from puppy.search import SearchEngine

class SearchEngineManager(object):
  """Manages a collection of search engines the Pipeline Manager can act upon"""
  
  def __init__(self):
    """Constructor for SearchEngineManager."""
    self._search_engines = {}

  def _contains(self, search_engine_name):
    """ Check if a specified search engine is currently stored """
    if search_engine_name in self._search_engines:
      return True
    else:
      return False

  def get_search_engine(self, search_engine_name):
    """ If the specified search engine is stored return it, otherwise, return None """
    if self._contains(search_engine_name):
      return self._search_engines[search_engine_name]
    else:
      return None

  def get_search_engines(self):
    """ Return all the currently stored search engines """
    return self._search_engines

  def add_search_engine(self, search_engine_name, search_engine):
    """ Adds a search engine to the Pipeline Manager if it's valid and not already stored by the Manager """
    if self._contains(search_engine_name):
      print "Failed to add search engine because a search engine of the name '{0}' has already been added".format(search_engine_name)
    elif isinstance(search_engine, SearchEngine):
      self._search_engines[search_engine_name] = search_engine
    else:
      raise TypeError('%s (type=%s) not search engine' % (search_engine, type(search_engine)))

  def remove_search_engine(self, search_engine_name):
    """ Removed a search engine from the Pipeline Manager if it's currently stored by the Manager """
    if self._contains(search_engine_name):
      del self._search_engines[search_engine_name]
    else:      
      print "Failed to delete a search engine of the name '{0}' as there is no such search engine stored".format(search_engine_name)

  def clear_search_engines(self):
    """ Remove all existing search engines. """
    self._search_engines = {}