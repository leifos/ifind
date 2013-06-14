# -*- coding: utf8 -*-

import string
from puppy.result import ResultFilter


class ExclusionFilter(ResultFilter):
  """
  Filters search results based on a list of words to exclude, if any of these are found the
  result in question is rejected.
  
  Options:
  
  * order (int): defines when, in the pipeline, this filter will be executed

  * terms (str): terms that, if appearing in the result, will cause it to be rejected - separated by "+'s"

  * customFields (list of str): extra fields in the results to filter with the exclusion list - depedendent upon their existence in the search service results

  """
  
  def __init__(self, order=0, terms="", customFields=[]):
    """Constructor for ExclusionFilter."""

    super(ExclusionFilter, self).__init__(order)
    self.info = "Filters search results based on a exclusion list."
    self.exclusion_list_string = " ".join(filter(str.isalpha, terms.replace('+', ' ').lower().split()))
    self.filter_fields = ['title', 'summary'] # Default fields we always have - ala opensearch and PuppyIR standard
    for field in customFields:
        self.filter_fields.append(field)
  
  def matches_exclusion_list(self, input_string):
    """
    Removes results that includes words contained in exclusion list.
    
    Parameters:
      
    * exclusion_list_string: terms which, if found, will cause a result to be rejected
    * input_string: string with words separated by blank spaces i.e. the result field being checked for terms from the exclusion list 
    
    Returns:
    
    * true: if any of the words of the input string is included in the exclusion list 
      false: in other case          
    """
    input_list = input_string.split()
    exclusion_list = self.exclusion_list_string.split()

    for input in input_list:  
      try:  
        input_filtered = "".join(filter(str.isalpha, list(input.lower())))
      except TypeError:
        tmp = input.encode("utf-8").lower()
        input_filtered = "".join(filter(str.isalpha, list(tmp)))

      # JMG Bug corrected 
      # We need to test for a string (the input word) in a list (the blacklist), not for a string in a string
      # If we check for a sting in a string, we check for any substring, so for instance, "pup" is in "puppy",
      # so we'd filter too much results
      if input_filtered in exclusion_list:
        if input_filtered not in ' ':
          return True
      
    return False


   
  def filter(self, results): 
    """
    Filters the results according to exclusion list - rejecting results containing offending words.

    Parameters:

    * results (puppy.model.Opensearch.Response): results to be filtered

    Returns:

    * results_returned (puppy.model.Opensearch.Response): filtered results
    """

    def fieldValid(result, field):
        """ This method checks the custom field exists and is also of format str/unicode """
        if(result.has_key(field)):        
            if (type(result[field]) == str or type(result[field]) == unicode):
                return True
            else:
                print('Error: custom field {0} was of {1} instead of str/unicode'.format(field, type(result[field])))
                return False
        else:
            print('Error: custom field {0} was not found in the results'.format(field))
            return False

    # Go through each result and check each field doesn't contain words in the exclusion list
    for result in results:
        valid = True
        for field in self.filter_fields:
            if fieldValid(result, field):
                valid = not (self.matches_exclusion_list(result[field]))
            if valid == False:
                break

        if (valid == True):
            yield result
       
