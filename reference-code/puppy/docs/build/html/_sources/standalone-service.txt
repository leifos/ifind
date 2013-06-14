.. _building-a-standalone-puppyir-service:

Building a Standalone PuppyIR Service
===========================================

The PuppyIR framework can, in addition to being used in combination with frameworks like Django (this is detailed later in the :ref:`building-a-puppyir-django-service`), be used to build a standalone services with no graphical user interface. This is a good place to start when initially developing with PuppyIR and can also be more appropriate for experimental development of new child-friendly information processing components.

This section assumes that you have read the section of the search service paradigm (if not, read it now before going any further: :ref:`service_architecture`) and are familiar with its various components.

The following steps will create and configure a new service, consisting of: a search engine, a query logger, a query pipeline, a result pipeline and query suggestions. The code comments note where new lines of code are and what they do.

Create and configure a ServiceManager
------------------------------------------------------

Create a new python script called *service.py* and add the following lines of code to it to create a service manager:

::

  from puppy.service import ServiceManager
  
  config = {} # See note below on Proxy Servers
  
  # Create the ServiceManager
  sm = ServiceManager(config)

N.B. if you require this standalone service to go through a proxy server, amend the config line of code to:

::

  config = {"proxyhost": "http://your-proxy-server-address"}

Create a SearchService
------------------------------------------------------

Next, we will create a search service to add to our service manager ready to retrieve results. Amend your code so it matches the following:

::
  
  # We now need to import SearchService as well
  from puppy.service import ServiceManager, SearchService
  
  config = {}
  
  sm = ServiceManager(config)
  
  # Create SearchService and give it a name
  ss = SearchService(sm, "bing_web")
  
  # Add our new SearchService to ServiceManager
  sm.add_search_service(ss)

Add a SearchEngine
------------------------------------------------------

Of course, our search service has not yet been linked to a search engine wrapper, let's link it to Bing by amending the code like so:

::

  from puppy.service import ServiceManager, SearchService

  # Import PuppyIR's Bing search engine wrapper
  from puppy.search.engine import Bing
  
  config = {}
  
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  
  # Set our SearchService to use the Bing wrapper
  ss.search_engine = Bing(ss)
  

Perform a Search
------------------------------------------------------

At this stage, we can now use the service we have created to search using Bing and retrieve results. Let's add some code to handle this and output the results to console:

::

  from puppy.service import ServiceManager, SearchService
  from puppy.search.engine import Bing

  # Import PuppyIR's Query and Response models
  from puppy.model import Query, Response
  
  config = {}
  
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  ss.search_engine = Bing(ss)
  
  # Construct a query object for the query term puppy
  query = Query("puppy")

  # Retrieve the results from our SearchService (.entries are the results in a Response)
  results = sm.search_services['bing_web'].search(query).entries
  
  # Go through each result and output the title, summary and link they contain
  for result in results:
    print result['title']
    print result['summary']
    print result['link']
    print '\n'

Enable the QueryLogger
------------------------------------------------------

It may be useful to start logging queries to file so we can keep track of our query history:

::

  from puppy.service import ServiceManager, SearchService
  from puppy.search.engine import Bing
  from puppy.model import Query, Response

  # Import PuppyIR's QueryLogger
  from puppy.logging import QueryLogger
  
  # Add a log_dir and set the path to it in config
  config = {"log_dir": "/path/to/log/directory"}
  
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  ss.search_engine = Bing(ss)
  
  # Assign a QueryLogger to our SearchService
  ss.query_logger = QueryLogger(ss, log_mode=0)
  
  query = Query("puppy")
  results = sm.search_services['bing_web'].search(query).entries
  
  for result in results.entries:
    print result['title']
    print result['summary']
    print result['link']
    print '\n'

Adding a QueryModifier and a ResultFilter
------------------------------------------------------

Now that we have an application that retrieves results up and running let's tailor it to suit children. First, we'll add a query modifier to append 'for kids' to all our queries and second, a suitability result filter to remove unsuitable results (for children):

::

  from puppy.service import ServiceManager, SearchService
  from puppy.search.engine import Bing
  from puppy.model import Query, Response
  from puppy.logging import QueryLogger

  # Import the modifier and filter mentioned above
  from puppy.query.modifier import TermExpansionModifier
  from puppy.result.filter import SuitabilityFilter
  
  config = {"log_dir": "/path/to/log/directory"}
  
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  ss.search_engine = Bing(ss)
  ss.query_logger = QueryLogger(ss, log_mode=0)
  
  # Add a TermExpansionModifier to SearchService
  ss.add_query_modifier(TermExpansionModifier(terms='for+kids'))

  # Add a SuitabilityFilter to SearchService - see note below on threshold
  ss.add_result_filter(SuitabilityFilter(threshold=0.5))
  
  query = Query("puppy")
  results = sm.search_services['bing_web'].search(query).entries
  
  for result in results.entries:
    print result['title']
    print result['summary']
    print result['link']

    # Print out the score each result (that was accepted) received
    print result['suitability']

    print '\n'

N.B. this filter works out a score for each result, which ranges from: 0.0, not suitable for children to 1.0, very suitable for children. The threshold defines the cutoff score for whether a result is accepted or rejected (i.e. only accept results with a score greater than 0.5). Try playing about with different settings for the threshold and investigate which results don't make the cut.

Multiple Search Services
------------------------

Whilst searching one source is useful, there are many possible situations in which a PuppyIR based service might need to search multiple sources.  The simplest example, is a service that provides search suggestions alongside the main search results. The search suggestions may come from a completely different source, but, in this case, they come from a separate instance of Bing with a different source type: 'relatedSearch' (which retrieves query suggestions). Amend your code to match the following code and try out a few queries to see what suggestions you receive:

::

  from puppy.service import ServiceManager, SearchService
  from puppy.search.engine import Bing
  from puppy.model import Query, Response
  from puppy.logging import QueryLogger
  from puppy.query.modifier import TermExpansionModifier
  from puppy.result.filter import SuitabilityFilter
  
  config = {"log_dir": "/path/to/log/directory"}
  
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  ss.search_engine = Bing(ss)
  ss.query_logger = QueryLogger(ss, log_mode=0)
  
  ss.add_query_modifier(TermExpansionModifier(terms='for+kids'))

  ss.add_result_filter(SuitabilityFilter(threshold=0.0))

  # Create a new SearchService for our query suggestions service
  suggestions_service = SearchService(sm, "suggestion_search")

  # Set our new SearchService to use the Bing wrapper with RelatedSearch
  suggestions_service.search_engine = Bing(suggestions_service, source = "RelatedSearch")

  # Add our new SearchService to our ServiceManager
  sm.add_search_service(suggestions_service)
  
  query = Query("puppy")
  results = sm.search_services['bing_web'].search(query).entries

  # Retrieve our query suggestions
  suggestions = sm.search_services['suggestion_search'].search(query).entries
  
  for result in results.entries:
    print result['title']
    print result['summary']
    print result['link']
    print result['suitability']
    print '\n'

  # Go through and print out our query suggestions to console
  for result in suggestions:
    # The title is the query suggestion, i.e. for Batman a suggestion could be: Batman Begins
    print result['title']