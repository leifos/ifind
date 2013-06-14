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

class QueryLogger(object):
  """Logs queries for a SearchService.
  
  The QueryLogger will log all queries submitted to a SearchService, sending them to:
  
  a) current directory, if there is no given log_dir
  b) specific directory, if a log_dir filepath is given (by constructor or config)
  
  The QueryLogger has five logging modes:
  
  a) OneBigFile - single file that grows endlessly
  b) Rotational - files rotate when log file size is = 1GB
  c) Timed - files rotate every day at midnight
  d) Permanent Rotating - files rate when the log file size is reached taking a unique name for each new log
  e) Gzip Permanent Rotating - same as above by using Gz compression
  
  """
  def __init__(self, search_service, log_mode=0, log_dir=None, log_period='midnight', log_maxbytes=1000000000):
    super(QueryLogger, self).__init__()
    self.search_service = search_service
    self.log_mode = log_mode
    self.log_dir = log_dir if log_dir else self.get_log_dir()
    self.log_period = log_period 
    self.log_maxbytes = log_maxbytes
    self.query_logger = self.create_logger()
  
  
  def get_log_dir(self):
    """Find the log_dir if none was passed in the constructor.
    
    Checks the service config files, then defaults to creating 
    a log directory in the current working directory
    """
    if 'log_dir' in self.search_service.config:
      log_dir = self.search_service.config['log_dir']
      if os.path.exists(log_dir) is False:
        os.mkdir(log_dir)
      return log_dir
    else:
      log_dir = os.path.join(os.getcwd(), 'query_logs')
      if os.path.exists(log_dir) is False:
        os.mkdir(log_dir)
      return log_dir
    
  
  def create_logger(self):
    """Create a new logger with a specific handler"""
    query_logger = logging.getLogger(self.search_service.name)
    query_logger.setLevel(logging.DEBUG)
    log_name = self.search_service.name + "_query_log"
    log_filename = os.path.join(self.log_dir, log_name)
    
    if self.log_mode is ONEBIGFILE:
      handler = logging.FileHandler(log_filename)
      query_logger.addHandler(handler)
      return query_logger
    elif self.log_mode is ROTATING:
      handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=self.log_maxbytes)
      query_logger.addHandler(handler)
      return query_logger
    elif self.log_mode is TIMED:
      handler = logging.handlers.TimedRotatingFileHandler(log_filename, when=self.log_period)
      query_logger.addHandler(handler)
      return query_logger
    elif self.log_mode is PERMANENTROTATING:
      handler = PermanentRotatingFileHandler(log_filename, maxBytes=self.log_maxbytes)
      query_logger.addHandler(handler)
      return query_logger
    elif self.log_mode is GZIPROTATING:
      handler = GzipRotatingFileHandler(log_filename, maxBytes=self.log_maxbytes)
      query_logger.addHandler(handler)
      return query_logger
    else:
      handler = logging.handlers.NullHandler()
      query_logger.addHandler(handler)
      return query_logger
  
  
  def log(self, query, processed=False):
    """logs a query using a simple [ISO Timestamp, Query Terms] format"""
    if processed:
      self.query_logger.debug("{0}, {1}, {2}".format(datetime.today().isoformat(), 'Processed Query (post pipeline)', query.search_terms))
    else:
      self.query_logger.debug("{0}, {1}".format(datetime.today().isoformat(), query.search_terms))
  

