.. _pipeline-puppyir-tutorial:

Pipeline Tutorial: DeeSe (Detective Search)
=======================================================

Getting Started
---------------

If you have not installed the PuppyIR framework and/or Django, please go to :ref:`requirements_and_installation` to get everything set up. Also, before starting this tutorial, it is recommended that you read the background page on the pipeline paradigm (:ref:`pipeline_architecture`) as this provides a conceptual description of the various components and how they work together.

The first step is to checkout the latest version of the tutorial from the PuppyIR SourceForge page and run it with the following commands:

::

  $ svn co https://puppyir.svn.sourceforge.net/svnroot/puppyir/trunk/prototypes/deese-tutorial
  $ cd /path/to/deese-tutorial
  $ python manage.py runserver

N.B. depending on your OS and SVN version, you may need to add ' deese-tutorial' to the end of the above svn checkout command.
  
Now visit: http://localhost:8000/deese to see the initial version of the application.

If you get stuck at any point during this tutorial, please consult the *service-complete.py* file in the *deese* folder, this contains the "answer" to this tutorial; along with code comments explaining each step.

DeeSee background
-----------------

This tutorial is, in a sense, a companion piece to the BaSe and IfSe tutorials in that it shows how to implement similar functionality using the 'pipeline' paradigm. The scenario in this tutorial  concerns a situation where the 'pipeline' paradigm is more suited the application than the 'service' paradigm.

The scenario is: you are working on an application for a team of Detectives to enable them to investigate several suspects (who have been stealing data off online websites). These suspects are well versed in electronic communication and are keeping a watch on the search history of the Detective Agency (by looking at queries sent and for their names appearing in the results the Detectives are viewing). To this end, DeeSe aims to provide the ability to search multiple sources, but have queries and results modified to prevent the names of the suspects appearing.

Therefore, for all the search services being used, one specific pipeline (for queries and results) needs to be put in place to enforce the 'lack of the suspects name' rule. Now, with the 'service' paradigm we would need to construct this pipeline for each and every source, but could we do it a different way? This tutorial details how, using the 'pipeline' paradigm, this could be accomplished.

Creating our Pipeline Service
-----------------------------

The first step is to create a pipeline service for DeeSe, this has already been done for you; but note how to do it. Next we need to add a search engine to our pipeline service. Open up *service.py* in the DeeSe directory and enter the following code (after the comment saying start here) to add a Bing news wrapper:

::

  # Create our Pipeline Service
  pipelineService = PipelineService(config, "myPipeline")

  # ----------------------- Start Here -----------------------

  # Create a Bing Search Engine for news results and limit to 5 results
  bingNews = Bing(pipelineService, source='news', resultsPerPage=5)

  # Add Bing News to our search engine manager (this stores all our search engines)
  pipelineService.searchEngineManager.add_search_engine("News", bingNews)
  
We can now search for Bing News results using the DeeSe's search box. However, there is no filtering yet implemented... we should start creating our pipeline.

Setting up our query pipeline
--------------------------------------------

Currently our query pipeline is empty (it contains no filters or modifiers), so it will allow us to search using the suspects names; thus alerting them to the investigation. Lets stop this by constructing a query pipeline that will prevent this from happening. To this end, we're going to add a query filter called **BlackListFilter**, which will reject queries if they contain blacklisted word(s). Let's assume that the suspects are called: Bob and Nathan and get coding:

::

  # Let's define a variable storing the names of the suspects
  suspects = 'Bob Nathan' # Separated by spaces

  # Now let's create a black list query filter using the suspects variable
  blacklistF = BlackListFilter(terms=suspects)

  # Add it to our pipeline service's query pipeline
  pipelineService.add_query_filter(blacklistF)
  
Now, if you're confident this will work, let's try searching for 'Nathan the train job' - since one of the thefts involved a rail company. Did it work (you should get a message saying the query was rejected)? If it did, lets move onto the next stage; if not, check your code against the code above or ask for help.

But what about the results?
----------------------------

The other required condition was that the results returned should not contain the suspects names. To do this we need to create a result pipeline to process the results. Let's add a **BlackListModifier**, what this does is "censor" blacklisted words (by replacing them with \*'s); thus, we can use this to ensure the suspects names do not appear. While we're at it, lets also add a profanity filter to stop queries containing naughty words.

::

  # Let's add a Black List Modifier to alter the results
  blacklistM = BlackListResultModifier(terms=suspects)

  # Also, as an extra, let's stop any naughty words
  profanityF = WdylProfanityQueryFilter()

  # Now let's use the add filters method to add both in one go
  pipelineService.add_filters(profanityF, blacklistM)

Try it out, can you think of queries that, while not containing the suspects names, will return results containing their names?

For the purposes of the Detective Agencies internal monitoring, all queries, both un-processed and processed (after going through the query pipeline), should be logged. Let's add a query logger to our pipeline service and set it to log processed queries (as well as the un-processed queries).

::

  # Create a Query Logger and attach it to our Pipeline Service
  pipelineService.query_logger = QueryLogger(pipelineService)

  # Set post logging to true i.e. log processed queries (post query pipeline)
  pipelineService.postLogging = True

Now, search with both valid and invalid queries (i.e. ones that should be rejected). Open the log file (located in the **deese_logs** directory) and take a look at your query history. Note that queries that were not rejected are logged twice (un-processed and processed) and that rejected queries are only logged once. This is because when a query is rejected the search is aborted and so there never is a processed query. Also, since we never added any query modifiers the processed queries are the same as their un-processed counterpart.

Let's add some new search services
----------------------------------

Of course, just searching Bing News does not really offer the multiple search services required; let's add Wikipedia and Bing Web as well:

::

  # Create Bing Web and Wikipedia Search Engines (again, limiting to 5 results)
  bingWeb = Bing(pipelineService, source='web', resultsPerPage=5)
  wikipedia = Wikipedia(pipelineService, resultsPerPage=5)

  # Add our new Search Engines to our Search Engine Manager
  pipelineService.searchEngineManager.add_search_engine("Web", bingWeb)
  pipelineService.searchEngineManager.add_search_engine("Wikipedia", wikipedia)

Now search for something, notice that the results appear for all of these search engines using the name we supplied for the search engines, i.e. they have Web, Wikipedia, News as their titles. Also, we did not need to alter **views.py** to get results from the new search engines (which you would have to do if using the **service** paradigm). This is because we are using the *searchAll* method call; you could also search them one by one using *searchSpecific* - which makes use of the name of the search engine. Due to this, we can easily add and remove search engines as required.

As an extension task, to allow you to fully understand how DeeSe allows new search engines to be added, have a look at the **index.html** template. The Django template language code is fully commented, explaining the purpose of each line and how the results of each service are accessed & displayed (also note how the template only shows details about a search engine if it returned one or more results). This is an example of how the overall results dictionary (see: :ref:`pipeline_architecture`) can be processed by an application.

Next steps
-----------------

Congratulations, that's you completed the tutorial. However, there is more you could do with DeeSe:

* If you look in **views.py** you will notice that there is code for that looks for a variable called *offset* as well as a query. This is to allow for browsing between pages of results, what changes/additions would you have to make to implement this? [Hint: you will need to change the template]
* Styling, perhaps you could add more images and alter the style to suit the Detectives more?
* Extending the pipeline, what else could you add to DeeSe in both the query and result pipelines?
* Are there any other search services you could add: videos, images? [Hint: you will need to alter the template]