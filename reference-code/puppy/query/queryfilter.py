# -*- coding: utf8 -*-

from puppy.model import Query
from puppy.query.exceptions import QueryFilterError, QueryModifierError

def ensure_query(f):
    """ Decorator to apply to methods that accept a Query and return a Query
    (e.g. modify). Wraps function to convert arg to Query if it isn't, and to
    convert return object to Query if it isn't. """

    def _inner(*args, **kw):
        new_args = list(args)[:]
        self = args[0]
        query = args[1]
        if isinstance(query, basestring):
            new_args[1] = Query(query)
        elif not isinstance(query, Query):
            raise TypeError('%s (%s) not Query' % (query, type(query)))

        q = f(*new_args, **kw)
        if not isinstance(q, Query):
            q = Query(q)

        return q
    return _inner

class QueryOperator(object):
  """Abstract class for query filters."""
  
  def __init__(self, order=0):
    self.name = self.__class__.__name__
    self.description = ""
    self.order = order
    self.handleException = True   # If it fails should we continue or stop the pipeline

  def for_language(self, language):
      """ Allows picking new language. """
      return self


class QueryModifier(QueryOperator):
    """Base class for all query modifiers"""
    def __call__(self, *args):
        # shortcut for modify
        return self.modify(*args)

    @ensure_query
    def modify(self, query):
        raise NotImplementedError()


class QueryFilter(QueryOperator):
    """ Base class for filters that can reject queries, e.g., by detecting
    profanity. """
    def __call__(self, *args):
        return self.filter(*args)

    @ensure_query
    def filter(self, query):
        raise NotImplementedError()