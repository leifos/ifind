.. _service_architecture:

Paradigm 1 - One Pipeline, One Search Engine
===============================================

The core component of a PuppyIR based application is a search service in this paradigm. A search service contains a variety of individual components that, when combined together, allow for: searching , retrieving and processing the results - from a specific defined search engine. These search services are stored and managed by a service manager. The diagram below shows the structure of a search service from its owner, the service manager, to all the individual components contained within the search service.

.. figure:: images/puppy-service-architecture.png
   :align:   center

   *The basic architecture of a PuppyIR application, using the 'Search Service' paradigm.*

Description of the components
*****************************

The roles of the components are as follows:

* **Service Manager**: this is in charge of managing (adding and deleting) all the search services used by an application.
* **Config**: local configuration options (e.g. for proxies, API keys and log files).
* **Search Service**: a single search service, with its own query logger and distinct query & result pipelines.
* **Query Logger**: logs queries, sent to a search service, to file (available for both un-processed and processed query logging - more on this later).
* **Search Engine**:  this is the search engine wrapper for a specific 'search service' - e.g. a 'search service' that uses the YouTube search engine (wrapper).
* **Query Pipeline**: a collection of query filters and modifiers associated with a specific 'search service'.
* **Result Pipeline**: a collection of result filters and modifiers associated with a specific 'search service'.

Data flow in the 'Service' paradigm
***************************************

The diagram below shows the basic flow between a user issuing a query and their results being returned.

.. figure:: images/puppy-pipelines.png
   :align:   center

   *The basic data-flow in the 'Search Service' paradigm.*

The 'search service' is passed a query, by the user/client, via the search method in the 'search service' (simple search is also available; this skips the query and result pipelines). It then goes through the query pipeline, first running all the query filters and then all the query modifiers. The processed query is then passed to the 'search engine' (defined for the current 'search service') and the results retrieved using the search method contained in the 'search engine' wrapper. The results are then passed through the result pipeline, first by running all the result filters and then, finally, all the result modifiers. Following the completion of the 'result pipeline', the processed results are then returned to the user/client.

On Filters, Modifiers and Query Logging
***************************************

Within each of these pipelines (query and result) there are both filters and modifiers. Filters are executed first and then, following this, the modifiers are executed. 

The distinction between a filter and a modifier is as follows:

* **Filters**: these reject or accept a query, or result, based on a defined criteria. For example a blacklist filter rejects queries containing one or more blacklisted words.

* **Modifiers**: these change the content of a query, or result, based on a defined behaviour. For example, appending “for kids” to every query.

There are two points at which queries can be logged: before the query goes through the query pipeline and after (i.e. un-processed and processed). The default is to log queries before processing - if a query logger has been added. The code below shows how to add a query logger and set it so that processed queries are logged, in addition to un-processed ones:

::

  from puppy.logging import QueryLogger
  from puppy.service import ServiceManager, SearchService

  config = {"log_dir": "/path/to/log/dir"} # Sets the log directory
  sm = ServiceManager(config)
  ss = SearchService(sm, "bing_web")
  sm.add_search_service(ss)
  ss.search_engine = Bing(ss)

  # Assign QueryLogger to SearchService
  ss.query_logger = QueryLogger(ss)
  ss.postLogging = True # Activate post-pipeline query logging

The Query and Results formats
***********************************************

Referring to the data flow diagram above, the formats of a query and results are as follows:

* A query is in the 'Query' format (for more see: :ref:`puppy_query`).
* The results are in the 'Response' format (for more see: :ref:`puppy_response`); this is what is returned by the search call (for the search engine in question).

Both the Query and Response formats are implementations of the OpenSearch specification; for more details, see the links below:

* `OpenSearch Query <http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_Query_element>`_.
* `OpenSearch Response <http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_response_elements>`_.