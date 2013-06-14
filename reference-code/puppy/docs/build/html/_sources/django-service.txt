.. _building-a-puppyir-django-service:

BaSe Tutorial: Building a PuppyIR/Django Service
=======================================================

The BaSe (Basic Search Engine) tutorial details how to create an application using the Django web application framework and the PuppyIR framework. Before starting this tutorial, please ensure that you have followed the instructions on :ref:`requirements_and_installation` for installing the framework (and its dependencies) and have, in addition, installed Django.

For more information on Django and a more detailed explanation of the steps detailed in this tutorial, please refer to the `Django tutorial <https://docs.djangoproject.com/en/1.3/intro/tutorial01/>`_.

Creating a Django project and application
-----------------------------------------

First, browse to the directory you want to store BaSe in and run the following commands to create a Django project for our application:

::

    $ path/to/django/installation/django-admin.py startproject base
    $ cd base
    $ python manage.py runserver
    

Check it worked by loading up your browser and going to: http://localhost:8000. A standard Django success page should be displayed congratulating you on creating your first Django project.

Now, we will create an application within the BaSe project called WeSe (Web Search). It is important to note that applications, such as WeSe, cannot have the same name as the project they are part of. Run the following command from in the BaSe directory to create the WeSe application:

::

    $ python manage.py startapp wese

The next step is to amend the *settings.py* file in the BaSe folder to include WeSe in the BaSe project. Open this file and amend the installed applications section to look like this:

::

    INSTALLED_APPS = (
	    # All the other currently installed apps here
	    'wese',
	)

Configuring the WeSe application, adding a view and creating the templates
--------------------------------------------------------------------------

Add a new directory called *template* in the BaSe folder. In this folder create a file called *index.html*, then add the following html to it:

::

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html>
	  <head>
	    <title>WeSe (Web Search) - a BaSe application</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	  </head>
	  <body>
	    <div id="page">

	      <div id="header">       
	        <h1 id="title">WeSe (Web Search) - a BaSe application</h1>
	      </div> <!-- end header -->

	      <div id="searchbox">

	        <form action="/wese/query/" onsubmit="return validate_form(this)" method="post">

	          {% csrf_token %} <!-- cross-site request forgery protection -->

	          <input type="text" name="query" value="" id="query">

	          <input type="submit" value="Search" />

	        </form>

	      </div> <!-- searchbox -->

	      <div id="resultbox">

	        {% block main %}{% endblock %} <!-- placeholder block for results -->

	      </div> <!-- resultbox -->


	    </div> <!-- end page -->

	  </body>
	</html>

Now we need to amend *settings.py* in the BaSe directory to include this new template directory. Add the following lines of code at the top of the file:

::

    import os
    APP_DIR = os.getcwd()
	
This will set-up a variable with the current working directory, we can then use this to refer to the template directory's path relative to this variable (no need to hard code the absolute path). Amend the template directory's code (in *settings.py*) so it looks like this:

::

    TEMPLATE_DIRS = (
	    os.path.join(APP_DIR, 'templates')
	)

The last step is to add a url for WeSe, so that Django knows which view to fetch. Load the 'url.py' file in the BaSe directory and change it so it looks like this:

::

    urlpatterns = patterns('',
	    # Other URLs
	    (r'^wese/$', 'wese.views.index'),
	)

Now add the following code to *views.py* in the WeSe folder, this will return our index page (using the template we created earlier).

::

    # Django
    from django.template.context import RequestContext
    from django.shortcuts import render_to_response

    def index(request):
        """show wese index view"""
        context = RequestContext(request)
        return render_to_response('index.html', context)

Now go to: http://localhost:8000/wese and our index page will be displayed.

Getting and displaying search results using PuppyIR
---------------------------------------------------

Create a file called *service.py* in the WeSe directory. This will store all our web services and configure them. Put the following code in it:

::

    from puppy.service import ServiceManager, SearchService
    from puppy.search.engine import Bing
    from puppy.model import Query, Response

    config = {}

    # create a ServiceManager
    service = ServiceManager(config)

    # create a SearchService and choose the search engine
    bing_search_service = SearchService(service, "bing_web")
    bing_search_service.search_engine = Bing(bing_search_service)

    # add SearchService to ServiceManager
    service.add_search_service(bing_search_service)

Now we have to create a template to show our results, add a new template (in the same directory as *index.html*) called *results.html* and add the following html to it (this template will be added to index to display the results - see Django documentation for more details on how this is done).

::

    {% extends 'index.html' %}

	{% block main %}

	<p>Search Terms: <em>{{ query }}</em></p>

	    {% for result in results %}
	        <div class="result">
	        <div id="resulttitle">
			<a href="{{ result.link }}">
			<strong>{{ result.title }}</strong>
			</a>
		</div>
	        <div id="resultdescription">{{ result.summary }}</div>
	        <div id="resultlink">{{ result.link }}</div>
	        </div>
	    {% endfor %}

    {% endblock %}

We know need a view for WeSe to handle the receiving of a query, getting the results and then displaying them. Load *views.py* in the WeSe directory and add the following new imports and method:

::

    # From PuppyIR
    from puppy.model import Query, Response

    # From WeSe - get our service manager so we can search for results
    from wese.service import service
	
    def query(request):
        """show results for query"""
        user_query = request.POST['query']
        results = service.search_services['bing_web'].search(Query(user_query)).entries
        context = RequestContext(request)
        results_dict = {'query': user_query, 'results': results}
        return render_to_response('results.html', results_dict, context)

Finally, we need to add a new URL to deal with queries, load *urls.py* from the BaSe directory and amend the code to:

::

    urlpatterns = patterns('',
	    # Previous URL's - these are not shown for clarity reasons
	    (r'^wese/query/$', 'wese.views.query'),
	)

Now go to: http://localhost:8000/wese and try out a few queries. Congratulations, that's you created your first PuppyIR/Django web application!