import imp
import ifind.search.engines as engines
import ifind.search.cache as cache
from ifind.search.engines.exceptions import EngineException


class Engine(object):
    """
    Abstract class representing an ifind search engine.

    """
    def __init__(self, cache_type=None, proxies=None):
        """
        Engine constructor.

        Kwargs:
            cache_type (str): Type of cache to use i.e.'instance' or 'engine'.
            proxies (dict): Mapping of proxies to use i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"}.

        Raises:
            CacheException

        Usage:
            See EngineFactory.

        """
        self.name = self.__class__.__name__

        self.cache_type = cache_type
        if cache_type:
            self._cache = cache.QueryCache(self)

        self.proxies = proxies

    def search(self, query):
        """
        Public search method for an Engine instance, returning the results of a query argument.
        Caching handled here, true search implementation deferred to subclass '_search' method.

        Args:
            query (ifind Query object): Object encapsulating details of search query.

        Returns:
            ifind Response object: Object encapsulating a search request's results.

        Raises:
            CacheException

        Usage:
            query = Query('hello world')
            engine = EngineFactory('wikipedia')
            response = engine.search(query)

        """
        if self.cache_type:
            if query in self._cache:
                print "********************** cache"
                return self._cache.get(query)
            else:
                response = self._search(query)
                self._cache.store(query, response)
                print "********************** request"
                return response
        else:
            return self._search(query)

    def _search(self, query):
        """
        Abstract search method for an Engine instance, to be implemented by subclasses.
        Returns results of search request made from query argument.

        Args:
            query (ifind query Object): Object encapsulating details of search query

        Returns:
            ifind Response object: Object encapsulating a search request's results.

        Raises:
            See subclasses.

        Usage:
            Private method.

        """
        pass


def EngineFactory(engine_string, **kwargs):
    """
    Public class method that instantiates and returns an Engine subclass, keyed by
    the 'engine_string' argument.

    Args:
        engine_string (str): Name of Engine subclass to instantiate.

    Kwargs:
        Accepts kwargs defined by the Engine subclass being instantiated.

    Returns:
        ifind Engine object: Instance of parameterised Engine subclass

    Raises:
        EngineException, see subclasses.

    Usage:
        engine = EngineFactory('wikipedia')
        engine = EngineFactory('bing', cache_type='engine')

    """
    if not engine_string:
        raise EngineException("EngineFactory", "Engine string not supplied")

    # get path of subclass
    module_path = engines.__path__[0] + '/' + engine_string.lower() + '.py'

    # load subclass from path
    try:
        module = imp.load_source('engine', module_path)
    except IOError:
        raise EngineException("EngineFactory", "Engine '{0}' not found".format(engine_string))

    # return subclass, instantiated by kwargs
    return getattr(module, engine_string.lower().title())(**kwargs)