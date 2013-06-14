# -*- coding: utf8 -*-

import string
from puppy.result import ResultFilter


class DuplicateFilter(ResultFilter):
  """
  Filters search results and rejects ones already stored by an application. This is done by default by checking the link field
  of new results against a list of ones currently stored by the application. If found, they are rejected.

  Options:
  
  * order (int): defines when, in the pipeline, this filter will be executed

  * existing results (list of str): urls already stored in the application - we want to avoid getting these again.

  """
  
  def __init__(self, order=0, existingResults=[]):
    """Constructor for DuplicateFilter."""

    super(DuplicateFilter, self).__init__(order)
    self.info = "Filters search results and removes ones already stored by the application using this filter (link field used for this check)."
    self.existingResults = existingResults
   
  def filter(self, results): 
    """
    Filters search results and rejects ones already stored by the application using this filter (link field used for this check).

    Parameters:

    * results (puppy.model.Opensearch.Response): results to be filtered

    Returns:

    * results_returned (puppy.model.Opensearch.Response): filtered results
    """

    # Go through each result and check it's already in the system
    for result in results:
        found = False
        for url in self.existingResults:
            if (result['link'] == url):
                found = True
                break

        if (found == False):
            yield result
        else:
            print('Rejected result as already stored')
       
