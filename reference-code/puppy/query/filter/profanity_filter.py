from puppy.model import Query
from puppy.query.exceptions import QueryFilterError
from puppy.query import QueryFilter

import re
import urllib
import json
import urllib2


BAD_RESPONSE = False
#BAD_RESPONSE = 'No/malformed profanity response'


class WdylProfanityQueryFilter(QueryFilter):
    """
    Rejects queries containing profanity using WDYL (by Google).

    What this does is query the service, which returns a JSON response of true or false depending upon the presence, or not, of profanity.

    Warning: there is a marked delay in waiting for a response from this service - overuse can lead to poor performance.

    Parameters:

    * order (int): filter precedence
    """

    URL_BASE = 'http://www.wdyl.com/profanity?q=%s'

    def __init__(self, order=0):
        super(WdylProfanityQueryFilter, self).__init__(order=order)

    def filter(self, query):
        quoted = urllib.quote(unicode(query).encode('utf-8'))
        url = WdylProfanityQueryFilter.URL_BASE % quoted

        try:
            data = urllib2.urlopen(url).read()
        except urllib2.URLError as e:
            raise QueryFilterError(e)

        response = json.loads(data)
        if response is None:
            return BAD_RESPONSE

        res = response.get('response')
        if res is None:
            return BAD_RESPONSE

        if res == 'true':
            return BAD_RESPONSE

        elif res == 'false':
            return True

        # -> res not in ('true', 'false') I suppose this is technically
        # possible which is why I'm checking for it.

        return BAD_RESPONSE


class RegexProfanityFilter(QueryFilter):
    def __init__(self, order=0, word_filter_regex=''):
        """ Filter based on regex.
        
            :parameter word_filter_regex: a string or compiled regex to match
            against.

        """

        super(RegexProfanityFilter, self).__init__(order=order)
        if isinstance(word_filter_regex, basestring):
            self._badwords = re.compile(word_filter_regex)
        else:
            self._badwords = word_filter_regex

    def filter(self, query):
        if query is None:  # or not isinstance(query, Query):
            raise TypeError('%s is not a Query' % query)
        if self._badwords.findall(unicode(query)):
            return BAD_RESPONSE

        return True
