.. _wrappers:

Wrappers available in the PuppyIR Framework
==========================================================

The PuppyIR framework contains a number of varied search engine wrappers. In this section - an overview of these wrappers, in terms of their category, is provided in order to provide an easy access guide to what is available (to enable a developer to select what best suits the application they have in mind). This is intended as a supplement to the :ref:`api` section which contains details of the implementation of these wrappers.

Please note that wrappers can, and do, appear in multiple categories as some wrappers are more general purpose than other, more specific, services. Also, the generic 'web' results category is not listed but is provided by, for example, *'Bing'* please see the API guide for more.

Some of these wrappers require API keys (again, see the API reference for details) in these cases, this requires the developer to sign up for said key on the respective search service webpages for the API in question.

Book Services
--------------

* **'GoogleBooks'** this wrapper provides access to the Google Books data store, you can search for books and, in some cases, retrieve samples or whole books for reading (you need to embed the samples if used in an application).

Image Services
--------------

These wrappers provide the ability to search for and retrieve image results.

* **'Bing'** and **'BingV2'**
* **'Flickr'**
* **'Picassa'**

Information Services
--------------------

* **'Wikipedia'** and **'Simple Wikipedia'** allow the searching of wikipedia's database. They results consist only of a link, snippet (summary) and a title, hence, this is not suitable if you require a large amount of textual content; but ideal for providing a short description for children.

Location Based Searching
------------------------

These services allow for searching for: either results in a defined location or for a location itself.

N.B. Google Geocode should be used to retrieve the geo-coordinates and/or bounding box to use with the other services as their location based parameter(s).

For an example of this in action, a prototype (it should be noted, that this prototype was abandoned and the code is quite rough in addition to it not being styled) is available which you can download via:

::

  $ svn co https://puppyir.svn.sourceforge.net/svnroot/puppyir/branches/working/LSee LSee
  $ cd LSee
  $ python manage.py runserver

Visit: http://localhost:8000/lsee

* **'Flickr'** allows for the retrieval of geotagged images within a defined bounding box.
* **'Google Geocode'** this service allows results to be retrieved for locations, for example, if you search for 'Edinburgh' it will return details of the various Edinburgh's around the world (like their location/latitude).
* **'Twitter'** allows for the retrieval of geotagged tweets made within a box defined by a point - the origin - with a radius to define a box around the point.
* **'YouTubeV2'** allows for the retrieval of geotagged videos from within a box defined by a point - the origin - with a radius to define a box around the point.

Movie Services
--------------

* **'Rotten Tomatoes'** allows for the retrieval of details about movies like: the cast and aggregated review score etc.

Music Services
--------------

N.B. YouTube and YouTubeV2 are also, arguably, a music based services due to the large proportion of music based content.

* **'ITunes'**
* **'LastFM'**
* **'Soundcloud'**
* **'Spotify'**

News Services
-------------

These wrappers provide the ability to search for news stories

* **'Bing'** and **'BingV2'** allow for the searching of the 'news' results.
* **'Guardian'** is a wrapper for the search api of the UK based newspaper: the Guardian. While UK based this service also provides a large variety of stories about events the world over.

Social Network and Social News Services
---------------------------------------

* **'Digg'** a social news website for sharing items which are then rated by the community - this acting as a method of filtering the quality of results.
* **'Twitter'** a social network for posting short messages.

Spelling Suggestions and Dictionary based results
-------------------------------------------------

* **'BingV2'** using the 'spell' source type spelling corrections to a query.
* **'Wordnik'** this service provides a spelling correction feature, in addition to providing definitions of words and examples of words in context (via selections of text from various web pages).
* **'WebSpellChecker'** allows for searching for spelling corrections in a variety of languages - there is no extra information returned however just the spelling correction suggestion.

Video Services
--------------

These wrappers provide the ability to search for videos. It should be noted that Bing's search engine strongly favours YouTube results so there is a lot of overlap if both it and YouTube are used in the same application.

* **'BingV2'**
* **'YouTube'** and **'YouTubeV2'** results from YouTube come with an embed URL so they can be played in-line (as seen in the MaSe and aMuSeV3 prototypes).