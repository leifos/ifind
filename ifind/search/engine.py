import importlib
from ifind.search.cache import QueryCache
from ifind.search.engines import ENGINE_LIST
from ifind.search.exceptions import EngineLoadException


class Engine(object):
    """
    Abstract class representing an ifind search engine.

    """
    def __init__(self, cache_type=None, proxies=None):
        """
        Engine constructor.

        Kwargs:
            cache_type (str): type of cache to use i.e.'instance' or 'engine'.
            proxies (dict): mapping of proxies to use i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"}.

        Attributes:
            cache (QueryCache): instance of QueryCache, instantiated by cache_type arg

        Raises:
            CacheException

        Usage:
            See EngineFactory.

        """
        self.name = self.__class__.__name__

        self.cache_type = cache_type
        if cache_type:
            self._cache = QueryCache(self)

        self.proxies = proxies

    def search(self, query):
        """
        Public search method for an Engine instance, returning the results of a query argument.
        Caching handled here, true search implementation deferred to subclass '_search' method.

        Args:
            query (ifind Query): object encapsulating details of search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

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
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:
            See subclasses.

        Usage:
            Private method.

        """
        pass


class EngineFactory(object):
    """
    Public class representing an ifind search engine factory.

    Instantiates and returns an Engine subclass, keyed by
    the 'engine' argument, or None otherwise.

    Args:
        engine (str): Name of Engine subclass to instantiate.

    Kwargs:
        Accepted kwargs defined by the Engine subclass being instantiated.

    Returns:
        ifind Engine object: Dynamically dispatched instance of Engine subclass.

    Raises:
        EngineLoadException.
        See subclasses.

    Usage:
        engine = EngineFactory('wikipedia')
        engine = EngineFactory('bing', cache_type='engine')
        engine_list = EngineFactory().engines()

        """
    def engines(self):
        """
        Returns list of available engines.

        """
        return ENGINE_LIST

    def __contains__(self, engine):
        """
        Special containment override for 'in' operator.

        Usage:
            print 'bing' in EngineFactory() --> True

        """
        return engine.lower() in ENGINE_LIST

    def __iter__(self):
        """
        Implements iterator for EngineFactory, returning a single engine at a time.

        Usage:
            for engine in EngineFactory():
                print result

        """
        for engine in ENGINE_LIST:
            yield engine

    def __new__(cls, engine="", **kwargs):
        """
        Overrides object construction so as to bypass __init__ so to dynamically
        dispatch 'engine' subclass. See class docstring.

        """
        # if engine in subclass list, return instantiation
        if engine.lower() in ENGINE_LIST:
            module = importlib.import_module('ifind.search.engines.{}'.format(engine.lower()))
            return getattr(module, engine.lower().title())(**kwargs)

        # if 'engine' defined but not in supported list
        elif engine:
            raise EngineLoadException("EngineFactory", "Engine '{}' not found".format(engine.lower().title()))

        # if 'engine' undefined ("" or None)
        else:
            return super(EngineFactory, cls).__new__(cls)