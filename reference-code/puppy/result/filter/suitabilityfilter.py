# -*- coding: utf8 -*-

import subprocess

from puppy.result import ResultFilter

# Enable relative paths:
import os
rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

class SuitabilityFilter(ResultFilter):
  """
  Filters search results based on the results' suitability for children.
  
  Parameters:
  
  * order (int): filter precedence

  * threshold (double): confidence score to accept a page (e.g. 0.5)
  """
  
  def __init__(self, order=0, threshold=0.0):
    super(SuitabilityFilter, self).__init__(order)
    self.info = "Filters search results based on the results' suitability for children."
    self.threshold = threshold
  
  
  def filter(self, results):
    '''
    Filters the document list according to child suitability.
    
    Keeps only documents with a suitability confidence >= the specified threshold confidence.
    '''
    # Concatenate urls to classifier input string
    input = " ".join([entry['link'] for entry in results])
    
    # Call classifier from command line
    absolutePath = os.path.abspath(os.path.dirname(__file__))+"/"
    p1 = subprocess.Popen(["java", "-jar", rel("suitability_url.jar"), "-p", absolutePath, input], stdout=subprocess.PIPE)
    output = p1.stdout.readlines()
    
    # split output into {"url":score, ...}
    url_score_list = [urlscore.partition(" -> ") for urlscore in output]
    
    url_score_map = {}
    for key, sep, val in url_score_list:
      url_score_map.setdefault(key, float(val.rstrip()))
    
    # add score to existing results and filter by threshold
    for i, entry in enumerate(results):
      link = entry['link']
      score = url_score_map[link]
      if link in url_score_map:
        entry.setdefault('suitability', score)
      else: 
        entry.setdefault('suitability', None)
      if score >= self.threshold:
        yield entry
  
