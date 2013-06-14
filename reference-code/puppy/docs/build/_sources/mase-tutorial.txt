.. _mase-mash-up-search-engine-puppyir-tutorial:

MaSe Tutorial: Create Your Own Mash-Up Search Interface
=======================================================

Getting Started
---------------

Before starting this tutorial, we assume that you have downloaded and installed the PuppyIR framework along with required associated Python Libraries (this tutorial also requires Whoosh to be installed). If you have not installed the PuppyIR framework and/or Whoosh go to :ref:`requirements_and_installation` and get everything set up.

The MaSe tutorial is designed to show the PuppyIR framework can be used to create an interactive customisable web application, quickly, using the Django web application framework. No Python experience is required to do this tutorial, as there is minimal coding involved and there are instructions regarding what coding there is (failing that, an answer file is included called **complete-service.py** which includes working code for all the tasks).

Please note, that Javascript must be enabled for this tutorial to work, ask your teacher if this is the case and, if not, get them to enable Javascript for you.

You will also need a Bing Azure API key, you can sign up at https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44 and obtain a key for for free.

Downloading the Source Code for the Tutorial
++++++++++++++++++++++++++++++++++++++++++++

The first step is to download the latest release of the tutorial from the PuppyIR repository using the following command (if you have problems with this step please ask your teacher for help):

::

  $ svn co https://puppyir.svn.sourceforge.net/svnroot/puppyir/trunk/prototypes/mase-tutorial mase-tutorial

Run MaSe
++++++++

To run MaSe, execute the following two commands (substituting in the path to where you downloaded MaSe to):

::
  
  $ cd /path/to/mase-tutorial
  $ python manage.py runserver
  
Now, visit: http://localhost:8000/mase which should bring up the screen shown below (if you are using Internet Explorer you will not get rounded edges for your result boxes): 

.. figure::  images/mase-1-initial.png
   :align:   center

   *MaSe running on a local machine.*

To search for results either press enter/return in the search box or click on the magnifying glass. You will notice that no results are returned - this is because we have to construct a PuppyIR service and configure it to include a search engine.

You can customise several aspects of the MaSe search interface, as detailed below:

1. Clicking on the title, 'MaSe', allows you to change the name of the search engine by typing in a new name - pressing enter/return will save your search engine's new name.
2. Clicking on the paw images in the *Colour your search engine* box will change the colour theme.
3. You can also move the result boxes around on the screen (more on this in the next section).
4. Minimise results by clicking on the *-* on the top right of a result box; you can maximise it again by clicking on the *+* that appears when results are minimised.

Go ahead and name your search engine now and pick a new colour scheme - your new settings will be saved (using cookies; ask your teacher to enable cookies if they are disabled) so there is no need to do this every time.


Adding our first services
-------------------------

Since, we don't have any services added yet we wont get no results when searching. Let's fix that now by adding our first search service: web results. Open the **service.py** file in the *mase* directory and add the following lines of code, at the bottom of the file(the code comments, the lines starting with #, detail the purpose of each line of code):

::

  # create a SearchService, called 'web_search'
  web_search_service = SearchService(service, "web_search")

  # Set our SearchService to use the Bing search engine (it defaults to search for web results)
  web_search_service.search_engine = BingV3(web_search_service, source='Web')

  # add SearchService to our ServiceManager (this handles all the search services MaSe contains) 
  service.add_search_service(web_search_service)



Now that you have added the service you'll need to make sure you have entered your Bing Api key into the config:
::

  config = {
    ....
    ....
    "bing_api_key": "<--PUT YOUR BING API KEY HERE--->",
  }

You may also need to set the proxy in the config file. Ask your teacher if you need to add a proxy and add it to the config aswell.

Now, save this file and refresh your browser and search for something (try the query "puppies"). You should be presented with results, for your query, in a format similar to what is shown below:

.. figure::  images/mase-3-web.png
   :align:   center

   *Our now customised MaSe (custom title and new colour scheme) showing web results.*




Now, lets limit the number of web results to only three, this is done by changing the line of code shown below to:

::

  # Set the resultsPerPage parameter to 3; this limits the results the service will return
  web_search_service.search_engine = BingV3(web_search_service, source='Web', resultsPerPage = 5)

But it's boring just having one set of results - so lets add images as well. This is done by adding the code below (note the differences and similarities to adding web results):

::

  # create a SearchService, called 'image_search'
  image_service = SearchService(service, "image_search")

  # Set our SearchService to use Bing but this time with images
  image_service.search_engine = BingV3(image_service, source='Image', resultsPerPage = 5)

  # add SearchService to our ServiceManager
  service.add_search_service(image_service)

Go ahead and search for something, you should now see both image and web results displayed. You can also drag your results around and place them either on the left, centre, or right result columns; an example of this is shown below:

.. figure::  images/mase-4-webimages.png
   :align:   center

   *Re-arranging 'Web' and 'Image' results in MaSe.*

Extending MaSe with query logging and suggestions
--------------------------------------------------

Now let's add a query logger to record the queries that users submit.  Add the code below, just after where we created the web and image search services:

::

  # create a file based QUERY LOGGER
  web_search_service.query_logger = QueryLogger(web_search_service, log_mode=0)


Now save the file again, and try a few queries: "puppies", "kittens", "cats and dogs"...

This simple query logging component simply saves the queries that were entered into the a file called "web_search_query.log" and it is located in the directory mase-tutorial/mase/query_logs. Take a look at the query log.

This query logger is pretty simple, but what if we want to provide query suggestions. In this case, it would be preferable to save the queries that are entered into a query index, which we can search later on. To do this add the following lines of code:

::

  # Create a Whoosh Query Logger that records all the unique queries
  whoosh_query_logger = WhooshQueryLogger(whoosh_query_index_dir=whoosh_dir, unique=True)

  # Add the Whoosh Query Logger to the web_search service
  web_search_service.add_query_filter(whoosh_query_logger)


By adding this code, we now store all the queries in an index, which is housed in the directory: mase-tutorial/mase/query_logs/index

To provide suggestions to the user we need to add another search service, one which submits queries to this query index.
To enable this feature, add the following lines of code:

::

  # create a SearchService, called 'query_suggest_search'
  suggest_service = SearchService(service, "query_suggest_search")

  # Use the Whoosh Query Engine to record queries
  whooshEngine = WhooshQueryEngine(suggest_service, whoosh_query_index_dir=whoosh_dir)
  suggest_service.search_engine = whooshEngine

  # add SearchService to our ServiceManager
  service.add_search_service(suggest_service)

What the *suggest_service* does is to look at past queries and see if any of them contain terms from the current query. If so, it recommends those past queries as suggestions. The picture below shows query suggestions in action. Go ahead and enter a few queries now to test if the query suggestions are working. Please note, you may need to enter a few queries before any suggestions start appearing, as some queries need to be recorded before they can be recommended as suggestions.

.. figure::  images/mase-5-limitresults.png
   :align:   center

   *MaSe showing our now limited results for each service and query suggestions.*

Filtering and the Pipelining
--------------------------------------------------

Now that we've can retrieve results from three different sources (Web, Images, and Queries) we can begin to further customize our search services. By adding in the WhooshQueryLogger we added our first filter to the query pipeline.

Let's now add a query modifier to the query pipeline to stop users from submitting certain "blacklisted" terms. To do this after the creation of the *web_search_service*, add the following lines of code to add a **BlackListModifier** to remove inappropriate terms from queries:

::


  # Create a blacklist modifier to block queries containing the terms below
  query_black_list = BlackListModifier(terms = "bad worse nasty filthy")

  # Add our blacklist modifier to the web search service
  web_search_service.add_query_modifier(query_black_list)

Save the file and type in a few queries, like "bad puppy" or "bad kitty".  What happens to the results that you see?


You should notice that if you type in "bad puppy", you still get results for "bad puppy" from the image service. This is because we didn't add a **BlackListModifier** to our *image_service*. Do that now and make sure nothing nasty gets through.

Okay, so now try a few more queries similar to the ones you have already typed, "puppy", "nasty puppy", "puppy", etc. Do you notice anything strange about the query suggestions? Do they recommend queries that include the terms, "bad" or "nasty"?

This is not desireable, because we don't want to recommend inappropriate queries. The reason why this occurs is because we added the **BlackListModifier** after the **WhooshQueryLogger**, which means we first record the query before modifying it. Then when we querying the **WhooshQueryEngine** it retrieves these inappropriate queries.

Fix the order of the modifers and filters to avoid this problem. You may need to delete the query index in mase-tutorial/mase/query_logs/index (i.e. delete all files _MAIN_*.* in that directory).


.. figure::  images/mase-6-badsuggestions.png
   :align:   center

   *MaSe making bad suggestions and still showing image results; as in this case the filter was not added to image search*

Note that  **QueryLogger** we attached the web search service, by default logs all queries without the filters and modifiers applied. i.e. it is the raw query log. To log the processed queries, you need to set:
::

    web_search_service.postLogging = True


Further note that **QueryModifiers** are executed before **QueryFilters**.


Experimenting
--------------------------------------------------

Well done, that's you completed the tutorial. What's next is up to you, if you want to do more the following two sections contain details for suggestions for extending your search engine further.

Other Services
++++++++++++++

So far you've added images, web results and query suggestions to MaSe, but there's more available.

The table below details some other options for other search services that can be added to MaSe, see the code for *web_search_service* and adapt it using the details provided below:

+-----------------+-----------------+-----------------+-----------------+
| Result Source	  | Service Name    | Class Name      | Extra parameters|
+=================+=================+=================+=================+
|   Wikipedia     |  *wiki_search*  | **Wikipedia**   |                 |
+-----------------+-----------------+-----------------+-----------------+
|   Bing News     |  *news_search*  | **BingV3**      | source='News'   |
+-----------------+-----------------+-----------------+-----------------+
| Video (Youtube) | *video_search*  | **YouTubeV2**   |                 |
+-----------------+-----------------+-----------------+-----------------+
|     Twitter     | *twitter_search*| **Twitter**     |                 |
+-----------------+-----------------+-----------------+-----------------+

If you get stuck adding the above services, then look at the file **service-complete.py** which includes working code to add them.


