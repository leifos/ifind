from puppy.service import SearchService, ServiceManager
from puppy.search.engine import *
from puppy.model import Query, Response
from puppy.query import *
from puppy.query.filter import *
from puppy.result import *
from puppy.result.filter import *
from puppy.logging import QueryLogger
import sqlite3

# IMPORTANT:
# This class is obsolete now. It's here only for comparation of results.

# a caller code example
### Database connection
##database="puppy/interface/interface.db"
##con=sqlite3.connect(database)
###print con
##
##cs = ConfiguratedSearch(con, cf, "bing_web")
##
### construct a query
##q = Query('cat')
##
##
##
### Perform a web search on all SearchServices
##for result in cs.search(q):
##  print result

class ConfiguratedSearchSQL(object):

    def __init__(self,con,cf,name=""):
    
        cur = con.cursor()

        # create a ServiceManager
        self.sm = ServiceManager(cf)

        # create SearchServices
        self.search_service = SearchService(self.sm, name)


        # Add SearchServices to ServiceManager
        self.sm.add_search_service(self.search_service)

        # searching search engine in the database
        cur.execute("SELECT configuration_searchengine.searchEngine FROM configuration_searchengineused,configuration_searchengine  WHERE searchEngine_id = configuration_searchengine.id")

        entries = cur.fetchall()

        entry = entries[0]  #we only take the first search engine

        print "Search engine "+entry[0]

        cur.execute("SELECT key, value FROM configuration_parameters WHERE searchEngineUsed_id=1")

        parameters = cur.fetchall()

        dictPar = {}

        for parameter in parameters:
            dicPar[parameter[0]] = parameter[1]
    
        # Assign SearchEngine to SearchServices
        self.search_service.search_engine = globals()[entry[0]](self.search_service, **dictPar)


        #searching the QueryFilters
        cur.execute("SELECT numOrder, configuration_queryfilter.queryFilter, configuration_queryfilterorder.id  FROM configuration_queryfilterorder,configuration_queryfilter  WHERE queryFilter_id = configuration_queryfilter.id")

        entries = cur.fetchall()

        for entry in entries:
            try:
                ptr_func = globals()[entry[1]]
            except:
                print "Error: "+entry[i]+" not found"
                continue;
            
            cur.execute("SELECT key, value FROM configuration_parameterq WHERE queryFilterOrder_id="+str(entry[2]))

            parameters = cur.fetchall()

            dictPar = {}

            for parameter in parameters:
                dictPar[parameter[0]] = parameter[1]
                
            print "Query filter "+str(entry[0])+" "+entry[1]+" "+" "+str(dictPar)


            if(issubclass(ptr_func,QueryModifier)):
                self.search_service.add_query_modifier(globals()[entry[1]](**dictPar))
                print "QueryModifier"
            if(issubclass(ptr_func,QueryFilter)):
                self.search_service.add_query_filter (globals()[entry[1]](**dictPar))
                print "QueryFilter"
        

        cur.execute("SELECT numOrder, configuration_resultfilter.resultFilter, configuration_resultfilterorder.id FROM configuration_resultfilterorder,configuration_resultfilter  WHERE resultFilter_id = configuration_resultfilter.id")

        entries = cur.fetchall()

        for entry in entries:
            try:
                ptr_func = globals()[entry[1]]
            except:
                print "Error: "+entry[i]+" not found"
                continue;
                        
            cur.execute("SELECT key, value FROM configuration_parameterr WHERE resultFilterOrder_id="+str(entry[2]))

            parameters = cur.fetchall()

            dictPar = {}

            for parameter in parameters:
                dictPar[parameter[0]] = parameter[1]       
        
            print "Result filter "+str(entry[0])+" "+entry[1]+" "+str(ptr_func.__bases__)+" "+str(dictPar)

            if(issubclass(ptr_func,ResultModifier)):
                self.search_service.add_result_modifier(ptr_func(**dictPar))
                print "ResultModifier"
            if(issubclass(ptr_func,ResultFilter)):
                self.search_service.add_result_filter (ptr_func())
                print "ResultFilter"    
        # end 

    def search(self,query):
        return self.search_service.search(query)
      
