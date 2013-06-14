from puppy.result import ResultFilter

from urlparse import urlparse
import urllib


class BlacklistURLFilter(ResultFilter):
  """ Filters results from URLs on blacklist.

  Parameters:

  * blacklist (set or iterable): list of domains to filter, listed by site (not URL) (e.g., abc.com/d/e/f -> abc.com)

  * order (int): filter precedence

"""

  def __init__(self, blacklist, order=0):
    super(ResultFilter, self).__init__(order)
    if not isinstance(blacklist, set):
        blacklist = set(blacklist)

    self.blacklist = blacklist

  def filter(self, results):
    for result in results:
        if urlparse(result['link']).netloc in self.blacklist:
            continue
        yield result
