# -*- coding: utf8 -*-

from puppy.search import SearchEngine
from puppy.model import Query, Response
import pickle, os

class loadResponseFromFile(SearchEngine):
      """
      A 'fake' search engine, it doesn't connect to a search engine using internet, it loads a previusly saved Response object from a file. 

      This is useful for debugging and automated testing

      See also saveResponseToFileFilter

      Parameters:

      * path (string): is the normalized path the way './folder' or 'c://folder1/folder2'. The point before de right slash means 'this folder'.
      Also, the path given should be the absolute path to the file you want to use. This is due to the construction of the query object.
      The type of the file is determined by PickleSE and PickleFilter, so it's not necesary to add it.
      """
      
      def __init__(self, query):

            self.truePath = query.search_terms.split('/')
            self.fileName = self.truePath.pop(-1)
            self.folderPath = self.truePath.pop(0)
            for part in self.truePath:
                  self.folderPath = self.folderPath + '/' + part
                  
        
      def load(self, folp = '', filn = ''):
            """
            * folp (string) = folder path
            * filn (string) = file name
            Load the saved pickle results from the pickle folder.
            You can choose from a series of results under the same name or all the results. You can also choose only a specific result.
            The returning object should be a Response object. Due to the nature of the program can be any other the programmer has saved using the pickle_filter.
            In a similar way we can do with the pickleFilter, you can put the folder path directly in the loader and manage different folders or files. Should be the way: './folderpath' or 'c:/folder1/folder2/folder3/.../foldern'
            """
            if filn == '': filn = self.fileName
            elif folp == '': folp = self.folderPath
            
            try:
                  if os.path.isdir(folp + '/' ):
                        resp = pickle.load(open(folp + '/' + filn + '.p', "rb"))
                        if type(resp) != type(Response()):
                              print "The object in the Pickle file is not a Response Type. Be carefull"
                        return resp
            except IOError:
                  print "The path doesn't exist"
