.. _exceptionsInPuppyIR:

Exception Handling in PuppyIR
===================================

The PuppyIR framework provides a basic set of exceptions that handle errors that can occur in its components. These exceptions are split between errors that occur during the Query and Result pipelines, in addition to errors that occur within a search engine wrapper. This section details the handling of these exceptions and provides some examples.

Exception handling in the Query Pipeline
------------------------------------------

The following exceptions are available in this area of the framework:

* **Query Rejection Error**: used when a query is rejected due to it failing one or more query filter tests. For example, if a profanity filter is used and the users query contains a swear word, the query will be rejected. When catching this exception, callers should provide code to deal with this situation, as no results will be returned if this occurs.
* **Query Filter Error**: used when a filter operationally failed and the filter's function cannot be realised. Callers should respond to this as if a query rejection decision cannot be made.
* **Query Modifier Error**: used when a modifier operationally failed and the modifier's function cannot be realised. Callers should respond to this as if the query has not been modified as per the design of the developer.

They can all be imported with the following line of code:

::

  from puppy.query.exceptions import QueryRejectionError, QueryFilterError, QueryModifierError

An example of how to handle a query rejection error is detailed below:

::

  try:
    web_results = service.search_services['web_search'].search(query).entries
  except QueryRejectionError:
    # This variable can then be used to decide to show an error or the results
    result_dict['webQueryRejected'] = True

Exception handling for searching within an application
------------------------------------------------------

The following exceptions are available at this stage:

* **Search Engine Error**: used for handling issues arising from the operation of a search engine wrapper like proxy errors, the web service being down, invalid parameters etc. This is a general use exception that deals with any problems that might occur during the operation of a search engine wrapper.
* **API Key Error**: used only in a search engine wrapper that requires an API key (like BingV2), to ensure that the API key is supplied and has the correct field name.

They can both be imported with the following line of code:

::

  from puppy.search.exceptions import SearchEngineError, ApiKeyError

A **Search Engine Error** contains the option of printing out a formatted error message; as opposed to the default, of it being outputted as one line; an example of how to handle both of the search engine exceptions and make use of the formatted print is given below:

::

  formattedDesc = True
   # The searching code in the 'try' in simplified (full examples are found elsewhere)
  try:
    results = serviceManager.search_services['bing_web'].search(query).entries
  except SearchEngineError, e:
    if formattedDesc:
      print(e.formattedStr())
    else:
      print(e) # Unformatted is the default
  except ApiKeyError, e:
    print(e)

Exception handling in a search engine wrapper
----------------------------------------------------

The following two examples detail how to implement the exceptions detailed above, in the search engine wrapper itself. I.e. if you are extending this area of the framework (see: :ref:`extending_the_search_engine` for more details on adding a new search engine wrapper) or simple want to look at the code to understand what it's doing.

Below is an example of how to handle an API key Error:

::

  # Try and get the API key from config, if it's not there raise the error
  try:
    appId = self.service.config["bing_api_key"]
  except KeyError:
    # First parameter is the wrapper name, the second is the field name for the API key
    raise ApiKeyError("BingV2", "bing_api_key")

Below is an example of how to use the 'Search Engine Error' to deal with:

1. A urllib2 error and add in extra parameters for the error message.
2. A type error for some local variables.
3. A general catch-all error for anything unforeseen (this enables the **SearchEngineError** to be used in an application as a general catch all exception).

::

  try:
    # Omitted the code preceding the return statement see 'BingV2.py' for it in full
    return parse_bing_json('BingV2', query.search_terms, results, sources, pos)

  # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
  except urllib2.URLError, e:
    raise SearchEngineError("BingV2", e, errorType = 'urllib2', url = url)

  # Check for a type error for offset or resultsPerPage
  except TypeError, e:
    note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
    if isinstance(offset, int) == False:
      raise SearchEngineError("BingV2", e, note = note, offsetType = type(offset))

    if isinstance(self.resultsPerPage, int) == False:
      resultsType = type(self.resultsPerPage)
      raise SearchEngineError("BingV2", e, note = note, resultsPerPageType = resultsType)

    raise SearchEngineError("BingV2", e, url = url)

  # Catch all exception, just in case
  except Exception, e:
    raise SearchEngineError("BingV2", e, url = url)

You can pass a **SearchEngineError** exception as many extra parameters as required - since it uses a key/value args parameter, which enables extra information, specific to a particular wrapper, to be added and outputted as part of the exceptions error message.

Exception handling in the Result Pipeline
-------------------------------------------

The following exceptions are available at this stage:

* **Result Filter Error**: used when a filter operationally failed and the filter's function cannot be realised. Callers should respond to this as if a rejection decision cannot be made for the results of a query.
* **Result Modifier Error**: used when a modifier operationally failed and the modifier's function cannot be realised. Callers should respond to this as if the results have not been modified as per the design of the developer.

They can all be imported with the following line of code:

::

  from puppy.result.exceptions import ResultFilterError, ResultModifierError

Generic Error Handling
-------------------------------------------------------------

Error handling within a wrapper, filter or modifier is the responsibility of the developer that created the component. However, the PuppyIR framework does provide some basic generic exception handling. All of the components listed above contain a variable called *handleException* which defines if they should gracefully fail (e.g. if a query modifier fails then just return the un-modified query and continue) if there's a problem, or raise the exceptions listed above. You can set this for each individual component depending its importance, i.e. if our profanity filter fails, do we want to not return any results or continue on - despite the possibility of profanity in a query.