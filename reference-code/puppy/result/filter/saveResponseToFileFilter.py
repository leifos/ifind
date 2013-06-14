# -*- coding: utf8 -*-
from puppy.result import ResultFilter
import os, pickle

class saveResponseToFileFilter(ResultFilter):
  """
  Store the results from the search as a file, that can be loaded by loadResponseFromFile.

  This filter is useful for debugging and automated testing

  It only save and load it's own files. See loadResponseFromFile
  
  """

  def __init__(self, path = '.'):
    """
    Constructor for pickleFilter.
    
    Only saves the path where the pickle files should be.
    """
    self.path = path
    
  
  def save(self, item, name_folder = 'pickles', name_archive = 'pickle'):
    """
    Save the obtained results in the main folder (by defect)
    or in the specified folder. It will create a new folder
    containing the pickle results. It's name will be 'pickles'
    automaticly or the one given.
    
    The path given should be normalized with single right bars like:
    'D:/PuppyIR/hello' or './pickle' The dot means current folder.
    
    Item is the object or result where to store from. It will rewrite
    the archive if alredy exists.
    """
    if not os.path.isdir(self.path + '/' + name_folder):
      os.mkdir(self.path + '/' + name_folder)

    return pickle.dump(item, open(self.path + '/' + name_folder + '/' + name_archive + '.p', "wb", -1))
    

