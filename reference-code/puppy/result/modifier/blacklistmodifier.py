# -*- coding: utf8 -*-

import string
from puppy.result import ResultModifier


class BlackListResultModifier(ResultModifier):
	
  """
  Modify processes result entry content and replaces blacklisted words
  
  Options:

  * order (int): modifier precedence

  * terms (str): terms that, if appearing in the result, will be replaced with ***

  """
  
  def __init__(self, order=0, terms="", customFields=[]):
    """
    Constructor for BlackListResultModifier.

    Parameters:
 
    * order (int): filter precedence

    * terms (str): separated by + characters

    * customFields (list of str): extra fields in the results to modify - depedendent upon their existence in the search service results

    """

    super(BlackListResultModifier, self).__init__(order)
    self.info = "Modify search results based on a blacklist."
    self.terms = terms
    try:
      self.black_list_string = " ".join(filter(str.isalpha, terms.replace('+', ' ').lower().split()))
    except TypeError:
      tmp = terms.encode("utf-8").lower()
      self.black_list_string = " ".join(filter(str.isalpha, tmp.replace('+', ' ').lower().split()))
    self.modify_fields = ['title', 'summary'] # Default fields we always have - ala opensearch and PuppyIR standard
    for field in customFields:
        self.modify_fields.append(field)
  
  def apply_black_list(self, input_string):
    """
    Replaces words in black list for *** characters.
    
    Parameters:

    * black_list_string: string with words included in the black list
    * input_string: string with words separated by blank spaces 
    
    Returns:
    
    * ouput_string: string of words separated by blank spaces which 
    words included in the black list has been replaced by ***   
    
    """
    input_list = input_string.split()
    output_string = input_string

    for input in input_list:  
      try:  
        input_filtered = "".join(filter(str.isalpha, list(input.lower())))
      except TypeError:
        tmp = input.encode("utf-8").lower()
        input_filtered = "".join(filter(str.isalpha, list(tmp)))
             
      if input_filtered in self.black_list_string:
        if input_filtered not in ' ':
          output_string = output_string.replace(input, '***')
    return output_string

  def modify(self, results):
    """
    Filters the results according to black list - censoring any occuring blacklisted words in results.
    
    Parameters:
      
    * results (puppy.model.Opensearch.Response): results to be filtered
    
    Returns:
    
    * results_returned (puppy.model.Opensearch.Response): filtered results
          
    """   
    def fieldValid(result, field):
        """ This method checks the custom field exists and is also of format str/unicode """
        if field in result:
            #if(result.has_key(field)):         # <--- deprecated
            return isinstance(result[field], basestring)
#                return True
#            else:
            # XXX shouldn't this be an exception?
#                print('Error: custom field {0} was of {1} instead of str/unicode'.format(field, type(result[field])))
#                return False
        else:
            print('Error: custom field {0} was not found in the results'.format(field))
            return False
            

    # Go through each result and check each field doesn't contain words in the exclusion list
    for result in results:
        for field in self.modify_fields:
            if fieldValid(result, field):
                result[field] = self.apply_black_list(result[field])
        yield result
