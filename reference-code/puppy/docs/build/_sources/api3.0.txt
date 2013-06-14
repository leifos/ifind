.. _api:

PuppyIR API Reference
=====================

puppy.service
-------------

This module contains classes for building a service.

.. module:: puppy.service

ServiceManager
**************

.. autoclass:: ServiceManager
  :members:

SearchService
*************

.. autoclass:: SearchService
  :members:

puppy.pipeline
--------------

.. module:: puppy.pipeline

This module contains an alternate paradigm for creating a PuppyIR based service, where you construct one Pipeline, store multiple search engines and then either: search all or, search a specific one using the Pipeline. See: :ref:`pipeline_architecture` for an explanation of this paradigm and :ref:`pipeline-puppyir-tutorial` for details about how to go about using it to create an application.

PipelineService
***************

.. autoclass:: PipelineService
  :members:

SearchEngineManager
********************

.. autoclass:: SearchEngineManager
  :members:

puppy.search
------------

.. module:: puppy.search

SearchEngine
************

.. autoclass:: SearchEngine
  :members:

puppy.search.exceptions
-----------------------

.. module:: puppy.search.exceptions

SearchEngineError
*****************

.. autoclass:: SearchEngineError

ApiKeyError
*****************

.. autoclass:: ApiKeyError

puppy.search.engine
-------------------

.. module:: puppy.search.engine

.. _puppy_bing:

Bing
****

.. autoclass:: Bing

.. _puppy_bingV2:

BingV2 (API Version 2.2)
************************

.. autoclass:: BingV2

Digg
**********

.. autoclass:: Digg

EmmaSearch
**********

.. autoclass:: EmmaSearch

EmmaSearch SQL Server version
*****************************

A new version of the above (EmmaSearch) wrapper allowing for searching the Emma Hospital database using a Microsoft's SQL server.

Due to this SQL Server import being an extra (see the installation section for details about installing it), rather than required, you cannot import this wrapper from '*puppy.search.engine*' like the above wrappers; you import them using the code below:

::

  from puppy.search.engine.emmasearchMSSQL import EmmaSearchMSSQL

Flickr
**********

.. autoclass:: Flickr

Google Geocode
**************

.. autoclass:: GoogleGeocode

Google (depreciated)
********************

.. autoclass:: Google


Google Books
**************

.. autoclass:: GoogleBooks

Guardian
**********

.. autoclass:: Guardian

iTunes
**********

.. autoclass:: ITunes

LastFM
**********

.. autoclass:: LastFm

OpenSearch
**********

.. autoclass:: OpenSearch

Picassa
**********

.. autoclass:: Picassa

Rotten Tomatoes
***************

.. autoclass:: RottenTomatoes

SimpleWikipedia
***************

.. autoclass:: SimpleWikipedia

Solr
****

.. autoclass:: Solr

SoundCloud
**********

.. autoclass:: SoundCloud

Spotify
*******

.. autoclass:: Spotify

Twitter
*******

.. autoclass:: Twitter

WebSpellChecker
****************

Register for an API key here: http://www.webservius.com/services/spellcheck/spellcheck

.. autoclass:: WebSpellChecker

Wikipedia
*********

.. autoclass:: Wikipedia

Wordnik
*********

.. autoclass:: Wordnik

Yahoo
*****

.. autoclass:: Yahoo

.. _puppy_youtube:

YouTube
*******

.. autoclass:: YouTube

.. _puppy_youtubeV2:

YouTubeV2 (API Version 2.0)
***************************

.. autoclass:: YouTubeV2

Whoosh wrappers
---------------

The following two wrappers both require Whoosh to be installed, for instructions for installing Whoosh see :ref:`requirements_and_installation`.

Due to Whoosh being an extra, rather than required, you cannot import them from '*puppy.search.engine*' like the above wrappers; you import them using the code below:

::

  from puppy.search.engine.whooshQueryEngine import WhooshQueryEngine
  from puppy.search.engine.whooshQuerySuggestEngine import WhooshQuerySuggestEngine

Whoosh Query Engine
*******************
.. module:: puppy.search.engine.whooshQueryEngine
.. autoclass:: WhooshQueryEngine

Whoosh Query Suggest Engine
***************************

.. module:: puppy.search.engine.whooshQuerySuggestEngine
.. autoclass:: WhooshQuerySuggestEngine

puppy.model
-----------

.. module:: puppy.model

.. _puppy_response:

Response
********

.. autoclass:: Response
  :members:

.. _puppy_query:

Query
*****

.. autoclass:: Query
  :members:

Description
***********

.. autoclass:: Description
  :members:

puppy.query
------------------

.. module:: puppy.query

QueryFilter
***********

.. autoclass:: QueryFilter


QueryModifier
*************

.. autoclass:: QueryModifier

puppy.query.exceptions
-----------------------

.. module:: puppy.query.exceptions

QueryRejectionError
*******************

.. autoclass:: QueryRejectionError

QueryFilterError
*****************

.. autoclass:: QueryFilterError

QueryModifierError
******************

.. autoclass:: QueryModifierError

puppy.query.filter
------------------

.. module:: puppy.query.filter

BlackListFilter
***************

.. autoclass:: BlackListFilter

WDYL Profanity Filter
**********************

.. autoclass:: WdylProfanityQueryFilter

SuggestionFilter
****************
 
.. autoclass:: SuggestionFilter

WhooshQueryLogger
*****************

About the Whoosh Query Logger
+++++++++++++++++++++++++++++

The Whoosh Query Logger, like the search engine wrappers for Whoosh, requires Whoosh to be installed, for instructions for installing Whoosh see :ref:`requirements_and_installation`.

Due to Whoosh being an extra, rather than required, you cannot import it from '*puppy.query.filter*' like the above filters; you import the Whoosh Query Logger using the code below:

::

  from puppy.query.filter.whooshQueryLogger import WhooshQueryLogger

.. module:: puppy.query.filter.whooshQueryLogger
.. autoclass:: WhooshQueryLogger

puppy.query.modifier
--------------------

.. module:: puppy.query.modifier

.. _puppy_spelling_mod:

SpellingModifier
*********************

.. autoclass:: SpellingCorrectingModifier


TermExpansionModifier
*********************

.. autoclass:: TermExpansionModifier

KidsModifier
*********************

.. autoclass:: KidsModifier

KidifyQueryModifier
*********************

.. autoclass:: KidsModifier


puppy.result
-------------------

.. module:: puppy.result

ResultFilter
************

.. autoclass:: ResultFilter

ResultModifier
**************

.. autoclass:: ResultModifier

puppy.result.exceptions
-----------------------

.. module:: puppy.result.exceptions


ResultFilterError
*****************

.. autoclass:: ResultFilterError

ResultModifierError
*******************

.. autoclass:: ResultModifierError


puppy.result.filter
-------------------

.. module:: puppy.result.filter

Age Filter
****************

.. autoclass:: AgeFilter

Duplicate Filter
****************

.. autoclass:: DuplicateFilter

ExclusionFilter
****************

.. autoclass:: ExclusionFilter

ProfanityFilter
****************

.. autoclass:: WdylProfanityFilter


SuitabilityFilter
*****************

This filter evaluates a result on its suitability for children by assigning it a score of 0 (unsuitable) to 1.0 (100% suitable). For an example of how to use this filter check out the SeSu prototype - see :ref:`prototypes` for details on how to install and run this prototype.

N.B. this filter requires Java to be installed and present on the system path (see: :ref:`requirements_and_installation` for more).

.. autoclass:: SuitabilityFilter

puppy.result.modifier
---------------------

.. module:: puppy.result.modifier

BlackListModifier
*****************

.. autoclass:: BlackListResultModifier

URLDecorator
************

.. autoclass:: URLDecorator

puppy.logging
-------------

.. module:: puppy.logging

QueryLogger
***********

.. autoclass:: QueryLogger
  :members:

EventLogger
***********

.. autoclass:: EventLogger
  :members: