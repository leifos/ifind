# -*- coding: utf8 -*-

import os.path
import logging
import logging.handlers
from datetime import datetime
from puppy.logging.handlers import PermanentRotatingFileHandler, GzipRotatingFileHandler

ONEBIGFILE = 0
ROTATING = 1
TIMED = 2
PERMANENTROTATING = 3
GZIPROTATING = 4

class EventLogger(object):
  """
  
  The EventLogger will log all events submitted to it from an application (either standalone or Django)
  
  a) current directory, if there is no given log_dir
  b) specific directory, if a log_dir filepath is given by the constructor
  
  The EventLogger has three logging modes:
  
  a) OneBigFile - single file that grows endlessly
  b) Rotational - files rotate when log file size is = 1GB by default; can be changed via log_maxbytes
  c) Timed - files rotate every day at midnight
  d) Permanent Rotating - files rate when the log file size is reached taking a unique name for each new log
  e) Gzip Permanent Rotating - same as above by using Gz compression
  
  """
  def __init__(self, application_name, log_mode = 0, log_dir = None, log_period = 'midnight', log_maxbytes = 1000000000):
    super(EventLogger, self).__init__()
    self.application_name = application_name
    self.log_mode = log_mode
    self.log_dir = self.get_log_dir(log_dir)
    self.log_period = log_period 
    self.log_maxbytes = log_maxbytes
    self.event_logger = self.create_logger()
  
  def get_log_dir(self, log_dir):
    """
    Works out what the log directory will be. There are three cases:

    1) A log dir is given by the constructor and exits - use it
    2) A log dir is given by does not exist - make it and use it
    3) A log dir is not given then create one from current path
    """
    if log_dir:
      if os.path.exists(log_dir) is False:
        os.mkdir(log_dir)
      return log_dir
    else:
      log_dir = os.path.join(os.getcwd(), 'event_logs')
      if os.path.exists(log_dir) is False:
        os.mkdir(log_dir)
      return log_dir
    
  def create_logger(self):
    """Create a new logger with a specific handler"""
    event_logger = logging.getLogger(self.application_name)
    event_logger.setLevel(logging.DEBUG)
    log_name = self.application_name + "_event_log"
    log_filename = os.path.join(self.log_dir, log_name)
    
    if self.log_mode is ONEBIGFILE:
      handler = logging.FileHandler(log_filename)
      event_logger.addHandler(handler)
      return event_logger
    elif self.log_mode is ROTATING:
      handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes = self.log_maxbytes)
      event_logger.addHandler(handler)
      return event_logger
    elif self.log_mode is TIMED:
      handler = logging.handlers.TimedRotatingFileHandler(log_filename, when = self.log_period)
      event_logger.addHandler(handler)
      return event_logger
    elif self.log_mode is PERMANENTROTATING:
      handler = PermanentRotatingFileHandler(log_filename, maxBytes=self.log_maxbytes)
      event_logger.addHandler(handler)
      return event_logger
    elif self.log_mode is GZIPROTATING:
      handler = GzipRotatingFileHandler(log_filename, maxBytes=self.log_maxbytes)
      event_logger.addHandler(handler)
      return event_logger
    else:
      handler = logging.handlers.NullHandler()
      event_logger.addHandler(handler)
      return event_logger
  
  
  def log(self, identifier, action, **data):
    """
    Logs a query using a simple [ISO Timestamp, Identifier, Action, Data] format

    * Identifier (str): what identifies this log entry to a user i.e. IP address, Cookie Number etc

    * Action (str): the action the user has done i.e. page request

    * Data (str): associated data to the action done
    """
    eventData = ''
    for var in data:
        eventData += ", {0}:{1}".format(var, data[var])

    self.event_logger.debug("{0},{1},{2}{3}".format(datetime.today().isoformat(), identifier, action, eventData))
  

