import os
import sys

# if we are inside django, this is not necessary
if(not ('DJANGO_SETTINGS_MODULE' in os.environ)):
    APP_DIR = os.getcwd( )

    sys.path.insert(0,os.path.join(APP_DIR, 'puppy/interface'))

import settings

# if we are inside django, this is not necessary
if(not ('DJANGO_SETTINGS_MODULE' in os.environ)):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 


from django.db import models
from puppy.interface.configuration.models import *

from puppy.service import SearchService, ServiceManager
from puppy.search.engine import *
from puppy.model import Query, Response
from puppy.query import *
from puppy.query.filter import *
from puppy.query.modifier import *
from puppy.result import *
from puppy.result.filter import *
from puppy.result.modifier import *
from puppy.logging import QueryLogger

class ConfiguratedSearch(object):
    """Creates a search service taking data from a database"""    

    def __init__(self,cf,name="", dictParS={}):    
        """Constructor for the service.
    
        Parameters:
    
        * cf: dictionary with some enviromment vaulues (see ServiceManager)
        * name: a the name for the created search service  (see SearchService)
        * dictParS: a list of extra parameters for the search engine, in a dictionary format parameterName:value
        """
        #if we are outside Django, we need to define this here, not in the general settings.py as in a Django app.
        if(not (hasattr(settings, 'DATABASE_NAME'))):
            settings.DATABASES['default']['NAME'] = os.path.join(APP_DIR, 'puppy/interface/interface.db')
        else:
            settings.DATABASE_NAME = 'puppy/interface/interface.db'

        #print settings.DATABASES 

        # create a ServiceManager
        self.sm = ServiceManager(cf)

        # create SearchServices
        self.search_service = SearchService(self.sm, name)


        # Add SearchServices to ServiceManager
        self.sm.add_search_service(self.search_service)

        # searching search engine in the database
        #cur.execute("SELECT configuration_searchengine.searchEngine FROM configuration_searchengineused,configuration_searchengine  WHERE searchEngine_id = configuration_searchengine.id")

        entries = SearchEngineUsed.objects.all()

        entry = entries[0]  #we only take the first search engine

        print entry.searchEngine.searchEngine

        try:
            ptr_func = globals()[entry.searchEngine.searchEngine]    
        except:
            print "Error: "+str(entry)+" not found"
            

        #cur.execute("SELECT key, value FROM configuration_parameters WHERE searchEngineUsed_id=1")

 
        for parameter in ParameterS.objects.filter(searchEngineUsed = entry):
            print parameter
            dictParS[parameter.key] = parameter.value



        self.search_service.search_engine = ptr_func(self.search_service, **dictParS)    

        #searching the QueryFilters
        #cur.execute("SELECT numOrder, configuration_queryfilter.queryFilter, configuration_queryfilterorder.id  FROM configuration_queryfilterorder,configuration_queryfilter  WHERE queryFilter_id = configuration_queryfilter.id")

        entries = QueryFilterOrder.objects.all()

        for entry in entries:
            try:
                ptr_func = globals()[entry.queryFilter.queryFilter]    
            except:
                print "Error: "+str(entry)+" not found"
                continue; 

            dictPar = {}

            for parameter in ParameterQ.objects.filter(queryFilterOrder = entry):
                print parameter

                dictPar[parameter.key] = parameter.value

            print "Query filter "+str(entry.numOrder)+" "+entry.queryFilter.queryFilter+" "+" "+str(dictPar)

            if(issubclass(ptr_func,QueryModifier)):
                self.search_service.add_query_modifier(ptr_func(order=entry.numOrder,**dictPar))
                print "QueryModifier"
            if(issubclass(ptr_func,QueryFilter)):
                self.search_service.add_query_filter (ptr_func(order=entry.numOrder,**dictPar))
                print "QueryFilter"
##        
##
##        cur.execute("SELECT numOrder, configuration_resultfilter.resultFilter, configuration_resultfilterorder.id FROM configuration_resultfilterorder,configuration_resultfilter  WHERE resultFilter_id = configuration_resultfilter.id")
##
        entries = ResultFilterOrder.objects.all()

        for entry in entries:
            try:
                ptr_func = globals()[entry.resultFilter.resultFilter]    
            except:
                print "Error: "+str(entry)+" not found"
                continue; 

            dictPar = {}

            for parameter in ParameterR.objects.filter(resultFilterOrder = entry):
                print parameter

                dictPar[parameter.key] = parameter.value

            print "Result filter "+str(entry.numOrder)+" "+entry.resultFilter.resultFilter+" "+" "+str(dictPar)

            if(issubclass(ptr_func,ResultModifier)):
                self.search_service.add_result_modifier(ptr_func(order=entry.numOrder,**dictPar))
                print "ResultModifier"
            if(issubclass(ptr_func,ResultFilter)):
                self.search_service.add_result_filter (ptr_func(order=entry.numOrder,**dictPar))
                print "ResultFilter"
                

    def search(self,query):
        """Returns the search results. In turn, it calls the function in SearchService
    
        Parameters:
    
        * query (puppy.model.Query): search query
    
        Returns:
    
        * results (puppy.model.Response): search results
        """
        
        return self.search_service.search(query)
      
