import string
from puppy.result import ResultFilter

class AgeFilter(ResultFilter):
  """
  Filters search results based on either a specific age or if the age is within an age range defined by the result.

  Note: there is no default value for 'age' it must be passed to this filter so that it can be customised for the application using it. 
  
  Options:

  * order (int): filter precedence

  * age (integer) : the age of the user the results should be filtered for

  * ageField (str) : the field name for the age in the results

  * ageTolerance (int): if results just have an age field this defines the tolerance for accepting results i.e. within 3 years of the 'age' parameter - must be >= 0

  * maxAgeField (str) : the field name for the maximum age in the results

  * minAgeField (str) : the field name for the minimum age (if used)

  * rejectUnclassified (boolean): if set to true results without an age classificiation will be rejected automatically

  """
  
  def __init__(self, age, ageField = None, ageTolerance = 3, minAgeField = 'minAge', maxAgeField = 'maxAge', order = 0, rejectUnclassified = False):
    """Constructor for AgeFilter"""
    super(AgeFilter, self).__init__(order)
    self.age = age
    self.ageField = ageField
    self.ageTolerance = ageTolerance

    if self.ageTolerance < 0: # No negative age tolerances accepted
        self.ageTolerance = 0

    self.minAgeField = minAgeField
    self.maxAgeField = maxAgeField
    self.rejectUnclassified = rejectUnclassified
 
     
  def filter(self, results): 
    """
    Filters the results according to a given range in which the result is considered appropriate.

    Parameters:

    * results (puppy.model.Opensearch.Response): results to be filtered

    Returns:

    * results_returned (puppy.model.Opensearch.Response): filtered results
    """


    # Go through each result and check it matches the conditions defined
    for result in results:

        # If we only have an age field in the result then check if it fits in the defined range (set by the ageTolerance variable)
        if self.ageField and result.has_key(self.ageField):
            if result[self.ageField] >= (self.age - self.ageTolerance) and result[self.ageField] <= (self.age + self.ageTolerance):
                yield result

        # If we have a range in the result check if the age falls within this range
        elif result.has_key(self.minAgeField) and result.has_key(self.maxAgeField):
            if self.age >= result[self.minAgeField] and self.age <= result[self.maxAgeField]:
                yield result

        # If unclassified it depends upon the reject unclassified setting if we reject it or not
        else:
            if self.rejectUnclassified == False:
                yield result
