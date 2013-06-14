from puppy.model import Query
from puppy.query import ensure_query, QueryModifier
from puppy.query.exceptions import QueryModifierError

import lxml
import urllib2
import urllib


GS_URL = 'http://google.com/complete/search?output=toolbar&q=%s'


ENGLISH_MODIFIER_TERMS = 'for kids'
DUTCH_MODIFIER_TERMS = 'voor kids'


def _google_get(url):
    return urllib2.urlopen(url).read()


def gs_lookup(query):
    if isinstance(query, Query):
        quoted = query.url_quote()
    else:
        quoted = urllib.quote(query)

    url = GS_URL % quoted

    try:
        data = _google_get(url)
    except (urllib2.URLError, urllib2.HTTPError, IOError) as e:
        raise QueryModifierError(e)

    try:
        data = unicode(data, 'utf-8')
    except UnicodeDecodeError as e:
        return None

    try:
        parsed = lxml.etree.fromstring(data)
        for item in parsed:
            if len(item) == 0:
                continue

            if item[0] is None:
                return None

            data = item[0].get('data')
            if data is None:
                return None

            suggested = data.lower()
            if suggested == query:
                if len(item) > 1 and item[1] is not None:
                    try:
                        return int(item[1].get('int'))
                    except ValueError:
                        pass
                return 0
    except (lxml.etree.ParserError,) as e:
        raise QueryModifierError(e)

    return None


class KidsModifier(QueryModifier):
    """ 
    Base class for QueryModifiers aiming to modify queries to be more
    child-directed, e.g., appending for kids to query, creating Q -> Q.
    After modification, the Google Suggest service is checked for the
    presence of Q; if it exists as a frequenty query, Q is returned to
    the caller; otherwise, Q (the original query) is returned (hence a null
    operation).
    """

    def __init__(self, order=0, modifiers=None):
        # order modifiers by liklihood of success

        super(KidsModifier, self).__init__(order=order)

        if modifiers is None:
            modifiers = ENGLISH_MODIFIER_TERMS

        self._modifiers = modifiers

    @ensure_query
    def modify(self, query):
        return ('%s %s' % (unicode(query), self._modifiers))


class CheckedKidsModifier(KidsModifier):
    @ensure_query
    def modify(self, query):
        modified = super(CheckedKidsModifier, self).modify(query)

        if gs_lookup(modified) is not None:
            return modified

        return query


class DutchKidsModifier(CheckedKidsModifier):
    def __init__(self, order=0):
        """ Currently appends modifier terms, e.g., voor kinderen" in Dutch. """
        super(DutchKidsModifier, self).__init__(order, DUTCH_MODIFIER_TERMS)
#        super(DutchKidsModifier, self).__init__(order, ('voor kids', 'voor kinderen'))


class EnglishKidsModifier(CheckedKidsModifier):
    def __init__(self, order=0):
        """ Currently appends modifier terms, e.g., for kids" in English. """

        super(EnglishKidsModifier, self).__init__(order, ENGLISH_MODIFIER_TERMS)
#        super(EnglishKidsModifier, self).__init__(order, ('for kids', 'for children'))
