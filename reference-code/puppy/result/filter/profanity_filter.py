from puppy.result import ResultFilter
from puppy.query.filter.profanity_filter import WdylProfanityQueryFilter as WQF

import urllib


class WdylProfanityFilter(ResultFilter):
  """ Filters results with profanity in them by using the wsdl service.

    Pros:
      * no hardcoded blacklist. they do the effort in keeping the service
        effective

    Cons:
      * URL call. This can mean delay. Effort should be made to parallelize the
        pipeline so that this effect is minimal.

  Parameters:

  * order (int): filter precedence

  * customFields (list of str): extra fields in the results to filter with the
    exclusion list - depedendent upon their existence in the search service
    results

"""

  def __init__(self, order=0, customFields=[]):
    super(WdylProfanityFilter, self).__init__(order)
    self._filter = WQF()

    # Default fields we always have - ala opensearch and PuppyIR standard
    self.filter_fields = ['title', 'summary']

    for field in customFields:
        self.filter_fields.append(field)

  def filter(self, results):
        # call the existing one query filter

    def fieldValid(result, field):
        """ This method checks the custom field exists and is also of format
        str/unicode """

        #if(result.has_key(field)): # <- deprecated
        if field in result:
            numTerms = len(result[field].split())
            if isinstance(result[field], basestring) and numTerms <= 32:
                return True
            else:
                if numTerms > 32:
                    print('Error: Field {0} was longer than the 32 term limit for WDYL'.format(field, type(result[field])))
                else:
                    print('Error: Field {0} was of {1} instead of str/unicode'.format(field, type(result[field])))
                return False
        else:
            print('Error: Field {0} was not found in the results'.format(field))
            return False

        # Go through each result and check each field doesn't contain words in the exclusion list
    for result in results:
        valid = True
        for field in self.filter_fields:
            if fieldValid(result, field):
                valid = self._filter(result[field])
            if not valid:
                break
        else:
            yield result
