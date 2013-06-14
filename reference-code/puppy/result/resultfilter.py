# -*- coding: utf8 -*-

from puppy.result.exceptions import ResultFilterError, ResultModifierError

class Orderable(object):
  def __init__(self, order=0):
    self.order = order
    self.handleException = True  # If it fails should we continue or stop the pipeline
    self._init()

  def _init(self):
    raise NotImplementedError()


class ResultFilter(Orderable):
  """Abstract result filter."""
  
  def _init(self):
    self.name = self.__class__.__name__
    self.description = ""

  def __call__(self, *args):
    return self.filter(*args)
    
  def filter(self, results):
    """ Return a boolean of whether this filter succeeded. """

    raise NotImplementedError()


class ResultModifier(Orderable):
  """ Change result. """

  def _init(self):
    self.name = self.__class__.__name__
    self.description = ""

  def __call__(self, *args):
    return self.modify(*args)

  def modify(self, results):
    """ Return a result, modified. """
    raise NotImplementedError()