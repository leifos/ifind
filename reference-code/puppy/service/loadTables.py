import os
import sys

APP_DIR = os.getcwd( )

sys.path.insert(0,os.path.join(APP_DIR, 'puppy/interface'))


#print sys.path

import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 


from django.db import models
from puppy.interface.configuration.models import *

from puppy.search.engine import *
from puppy.query import *
from puppy.query.filter import *
from puppy.query.modifier import *
from puppy.result import *
from puppy.result.filter import *
from puppy.result.modifier import *

def loadSearchEngines():

    settings.DATABASES['default']['NAME'] = os.path.join(APP_DIR, 'puppy/interface/interface.db')
      
    for item in globals():
        try:
            if(issubclass(globals()[item],SearchEngine)):
                print "Search engine "+item
                if SearchEngineM.objects.filter(searchEngine=item):
                    print "Existent object "+item
                else:
                    print "Inserting object "+item
                    b = SearchEngineM(searchEngine = item)
                    b.save()
        except TypeError:
            continue
        
def loadQueryFilters():

    settings.DATABASES['default']['NAME'] = os.path.join(APP_DIR, 'puppy/interface/interface.db')    
    
    for item in globals():
        try:
            if(issubclass(globals()[item],QueryOperator)):
                print "Query filter "+item
                if QueryFilterM.objects.filter(queryFilter=item):
                    print "Existent object "+item
                else:
                    print "Inserting object "+item
                    b = QueryFilterM(queryFilter = item)
                    b.save()                
        except TypeError:
            continue
                        

def loadResultFilters():
    for item in globals():
        try:
            if(issubclass(globals()[item],Orderable)):
                print "Search engine "+item
                if ResultFilterM.objects.filter(resultFilter=item):
                    print "Existent object "+item
                else:
                    print "Inserting object "+item
                    b = ResultFilterM(resultFilter = item)
                    b.save()                                
        except TypeError:
            continue

            
