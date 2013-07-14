import mock

from nose.tools import assert_equal
from nose.tools import assert_raises
from nose.tools import assert_not_equal

from ifind.search.engine import Engine, EngineFactory
from ifind.search.exceptions import EngineLoadException
from ifind.search.exceptions import EngineAPIKeyException
from ifind.search.exceptions import EngineConnectionException

Engine, EngineFactory, EngineConnectionException, EngineAPIKeyException, EngineLoadException


class TestEngineFactory(object):
    """
    Test suite for EngineFactory.

    """
    def test_engine_instantiation(self):
        """
        Checks that an engine has been successfully instantiated.

        """
        pass

    def test_engine_instantiation_fail(self):
        """
        Checks exception thrown when an engine can't be instantiated.

        """
        pass

    def test_engine_search_with_bad_query(self):
        """
        Checks exception thrown when an engine's search method is passed a bad query.

        """

    def test_engine_search_without_cache(self):
        """
        Checks that an engine can successfully search without a cache.

        """

    def test_engine_search_with_cache(self):
        """
        Checks that an engine can successfully search with a cache.

        """

    def test_engine_factory_engine_list(self):
        """
        Checks that 'EngineFactory().engines()' returns valid list of supported engines.

        """

    def test_engine_factory_containment(self):
        """
        Checks that EngineFactory's 'in' override works correctly.

        """

    def test_engine_factory_iterable(self):
        """
        Checks that EngineFactory's iterable special class method works correctly.

        """