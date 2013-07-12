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

    """
    def __init__(self, engine=None, **kwargs):
        """
        Constructor that instantiates and returns an Engine subclass, keyed by
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
        if engine:
            EngineFactory._dispatch(engine, **kwargs)
        else:
            return

    def engines(self):
        """
        Returns list of available engines.

        """
        return ENGINE_LIST

    @staticmethod
    def _dispatch(engine, **kwargs):
        """
        Returns instantiated Engine sublass instance.

        Args:
            engine (str): name of Engine subclass to instantiate

        KWargs:
            Accepted kwargs defined by the Engine subclass being instantiated.

        Returns:
            ifind Engine object: Dynamically dispatched instance of Engine subclass.

        Raises:
            EngineLoadException.
            See subclasses.

        Usage:
            Private method.

        """
        # if engine in subclass list
        if engine.lower() in ENGINE_LIST:
            # import module
            module = importlib.import_module('ifind.search.engines.{}'.format(engine.lower()))
            # return instantiated class
            return getattr(module, engine.lower().title())(**kwargs)
        else:
            raise EngineLoadException("EngineFactory", "Engine '{}' not found".format(engine.lower().title()))

    def __contains__(self, engine):
        """
        Special containment override for 'in' operator.

        Usage:
            print 'bing' in EngineFactory() --> True

        """
        return engine.lower in ENGINE_LIST