# -*- coding: utf8 -*-
from puppy.core.type_checking import check
from puppy.pipeline import SearchEngineManager
from puppy.query.queryfilter import QueryFilter, QueryModifier
from puppy.query.exceptions import QueryRejectionError, QueryFilterError, QueryModifierError
from puppy.search import SearchEngine
from puppy.result.resultfilter import ResultFilter, ResultModifier
from puppy.result.exceptions import ResultFilterError, ResultModifierError
from puppy.logging import QueryLogger

class PipelineService(object):
  """Models the configuration of a Pipeline (QueryFilters/Modifiers and ResultFilters/Modifiers) and the search engines using the Pipeline"""
  
  def __init__(self, config, name):
    """Constructor for PipelineService."""
    self.config = config
    self.name = name
    self.searchEngineManager = SearchEngineManager()
    self.query_logger = None
    self.postLogging = False
    self._init_filters()

  def _init_filters(self):
    self.query_filters = []
    self.query_modifiers = []
    self.results_filters = []
    self.results_modifiers = []

  def searchSpecificEngine(self, query, searchEngineName, offset=0):
    """
    Search a specific search engine only, if it's currently stored by our 'SearchEngineManager' using the query and result pipeline as currently defined.

    Parameters:

    * query (puppy.model.Query): search query
    * searchEngineName (str): the name of the search engine to search which will be searched if it's currently stored
    * offset (int): result offset

    Returns:

    * results_dict (dictionary of puppy.model.Response): the key being the name of the search egine and the value the reponse object
    """
	
    results_dict = {}
    searchEngine = self.searchEngineManager.get_search_engine(searchEngineName) # None if doesn't exist

    # If our search engine is actually stored by the Pipeline Manager then get the results from it
    if searchEngine:
      query = self._runQueryPipeline(query)
      results_dict[searchEngineName] = self._getResults(query, offset, searchEngine)

    return results_dict  
  
  def searchAll(self, query, offset=0):
    """
    Search all the search engines currently stored by our 'SearchEngineManager' using the query and result pipeline as currently defined.
    
    Parameters:
    
    * query (puppy.model.Query): search query
    * offset (int): result offset
    
    Returns:
    
    * results_dict (dictionary of puppy.model.Response): the key being the name of the search egine and the value the reponse object
    """
    results_dict = {}
    query = self._runQueryPipeline(query) # Only run this once, it's the same for each search engine

    # Loop through each search engine and add results to the dictionary
    for key, value in self.searchEngineManager.get_search_engines().iteritems():
      results_dict[key] = self._getResults(query, offset, value) # I.e. run the defined Result pipeline for the current search engine

    return results_dict

  def _runQueryPipeline(self, query):
    """ Run through the defined query pipeline and return either the processed query or raise an exception (QueryRejectionError) """
    # Log the query sent to the pipeline manager before any processing
    if self.query_logger:
      self.query_logger.log(query)

    # Run the query filter pipeline
    self._run_query_filters(query)

    # Run through the query modifier pipeline and get the modified query back
    query = self._run_query_modifiers(query)

    # Log the query after processing (if it's not been rejected) if postLogging is enabled
    if (self.query_logger) and (self.postLogging == True):
      self.query_logger.log(query, processed=True) # Processed i.e. the query after going through the query pipeline

    return query # Return the modified query unless it was rejected

  def _getResults(self, query, offset, search_engine):
    """ Run through the defined result pipeline for the current search engine """
    
    try:  # Get the search results from the current search engine   
      results = search_engine.search(query, offset)
    except Exception, e:
      raise SearchEngineError("Test", e)
      
    search_results = results.entries
    
    # Run the result filter pipeline
    search_results = self._run_result_filters(search_results)
    
    # Run the result modifier pipeline
    search_results = self._run_result_modifiers(search_results)

    # Set the results entries to be the processed results then return them
    results.entries = search_results
    return results    
    
  def _run_query_filters(self, query):
    """This runs through all the filters in the query filter pipeline"""

    for query_filter in sorted(self.query_filters, key=lambda x: x.order, reverse=False):
      try:
        passed = query_filter(query)  # Did the query pass the current filter?
      except Exception, e:
        if query_filter.handleException:  # Should we ignore this?
          print "Handled Query Filter Error"
          return True
        else:                     # Or should we raise an exception?
          raise QueryFilterError()
      
      if passed != True:            # If it didn't, raise the Query Rejection Error
        raise QueryRejectionError(query)

  def _run_query_modifiers(self, query):
    """This runs through all the modifiers in the query modifier pipeline"""

    for query_modifier in sorted(self.query_modifiers, key=lambda x: x.order, reverse=False):
      try:
        query = query_modifier(query)
      except Exception, e:
        if query_modifier.handleException:  # Should we ignore this?
          print "Handled Query Modifier Error"
          continue
        else:                     # Or should we raise an exception?
          raise QueryModifierError()

    return query # Return the now modified query
    
    
  def _run_result_filters(self, search_results):
    """This runs through all the filters in the result filter pipeline"""

    for filt in sorted(self.results_filters, key=lambda x: x.order, reverse=True):
      try:
        search_results = filt(search_results)
      except Exception, e:
        if filt.handleException:  # Should we ignore this?
          print "Handled Result Filter Error"
          continue
        else:                     # Or should we raise an exception?
          raise ResultFilterError()

    return search_results

  def _run_result_modifiers(self, search_results):
    """This runs through all the modifiers in the result modifier pipeline"""

    for modifier in sorted(self.results_modifiers, key=lambda x: x.order, reverse=True):
      try:
        search_results = modifier(search_results)
      except Exception, e:
        if modifier.handleException:  # Should we ignore this?
          print "Handled Result Modifier Error"
          continue
        else:                     # Or should we raise an exception?
          raise ResultModifierError()

    return search_results

  def clear_filters(self):
    """ Remove all existing filters. """
    self._init_filters()

  def add_filters(self, *filters):
    """ Add one or more filters. Detects filter type (e.g., QueryFilter, ResultModifier) and places in appropriate pipeline. """
    for f in filters:
      dest = None
      if isinstance(f, QueryFilter):
        dest = self.query_filters
      elif isinstance(f, QueryModifier):
        dest = self.query_modifiers
      elif isinstance(f, ResultFilter):
        dest = self.results_filters
      elif isinstance(f, ResultModifier):
        dest = self.results_modifiers
      else:
        raise TypeError('%s (type=%s) not filter' % (f, type(f)))

      dest.append(f)

  def replace_filters(self, *filters):
    """ Replace existing filters with new filters. """
    self.clear_filters()
    self.add_filters(*filters)

  def add_query_modifier(self, query_modifier):
    """Add modifier to query modifier pipeline."""
    check(query_modifier, QueryModifier)
    self.query_modifiers.append(query_modifier)
  
  def add_query_filter(self, query_filter):
    """Add filter to query filter pipeline."""
    check(query_filter, QueryFilter)
    self.query_filters.append(query_filter)
  
  def add_result_filter(self, result_filter):
    """Add filter to result filter pipeline."""
    check(result_filter, ResultFilter)
    self.results_filters.append(result_filter)
  
  def add_result_modifier(self, result_modifier):
    """Add filter to result filter pipeline."""
    check(result_modifier, ResultModifier)
    self.results_modifiers.append(result_modifier)