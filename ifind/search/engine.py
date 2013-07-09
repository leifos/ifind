import imp
import ifind.search.engines as engines
import ifind.search.cache as cache
from ifind.search.engines.exceptions import EngineException


class Engine(object):
    """
    Abstract search engine interface.

    """
    def __init__(self, cache_type=None, proxies=None):
        """
        Constructor for SearchEngine.

        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)

        """
        self.name = self.__class__.__name__
        self._cache = cache.QueryCache(self, cache_type=cache_type)
        self.proxies = proxies

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        :param query: ifind.search.query.Query object
        :returns ifind.search.response.Response object
        :raises Requests bad url or something

        """
        if self._cache:

            if query in self._cache:
                print "********************** cache"
                return self._cache.get(query)

            response = self._search(query)
            self._cache.store(query, response)
            print "********************** request"
            return response

    def _search(self, query):
        pass


def EngineFactory(engine_string, **kwargs):

    if not engine_string:
        raise EngineException("EngineFactory", "Engine string not supplied")

    module_path = engines.__path__[0] + '/' + engine_string.lower() + '.py'

    try:
        module = imp.load_source('engine', module_path)
    except IOError:
        raise EngineException("EngineFactory", "Engine '{0}' not found".format(engine_string))

    return getattr(module, engine_string.lower().title())(**kwargs)