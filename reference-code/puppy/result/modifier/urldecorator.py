from puppy.result.resultfilter import ResultModifier

class URLDecorator(ResultModifier):
    """
    Decorates links to search results with given pre- and suffixes, returning [prefix]+url+[suffix].
    """
    
    def __init__(self, args, order=0):
      """
      Constructor for URLDecorator.
  
      Parameters:
  
      * prefix: String to preceed the original url.

      * suffix: String to tail the original url.
      """
      self.prefix = args[0]
      self.suffix = args[1]
      self.order = order

    def modify(self, results):
      """ 
      Returns a result set with modified urls.
      """
      for entry in results:
          entry['link'] = self.prefix+entry['link']+self.suffix
      return results