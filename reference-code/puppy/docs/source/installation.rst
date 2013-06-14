.. _requirements_and_installation:

Requirements and Installation
===================================

The PuppyIR framework is Python-based and requires, in addition to Python itself, several external dependencies. It can either be installed as a standalone service, or combined with the Django web application framework to build web services. The requirements, both basic and those required for additional functionality, are detailed here.

Note: if you are running MacOS X, please ensure that you have `X-Code <http://developer.apple.com/technologies/tools/>`_ installed (either Version 3 or 4; this may be included on your install disc). This is required as several of the dependencies use X-Code's C compiler.

PuppyIR and MacPorts
--------------------

For developers using MacOS X, `MacPorts <http://www.macports.org/>`_ can be used to install all the PuppyIR framework requirements. If you wish to install these using MacPorts please ensure that you install the *'py27'* versions. Please consult the MacPorts documentation for how to use MacPorts and then install all the basic and extra requirements (if required) using their port versions.

The one exception to the naming convention (of *'py27'*) is setuptools, which has the Port name **'py-setuptools'**.

.. _basic-requirements-label:

Basic Requirements
------------------

The basic PuppyIR framework installation requires all of the following to be installed (in addition to the framework itself):

* `Python Programming Environment <http://www.python.org/>`_ (N.B. Python 3.x is not supported)
* `Setuptools <http://pypi.python.org/pypi/setuptools>`_
* `Universal Feed Parser <http://code.google.com/p/feedparser/>`_
* `lxml <http://pypi.python.org/pypi/lxml/>`_
* `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/#Download>`_

.. _extra-requirements-label:

Extra Requirements
------------------

The following external dependencies are only required, if you intend to do any of the development tasks detailed below.

To create web services using the Django framework and/or to run the various prototypes and demonstrators:

* `Django Web Application Framework <https://www.djangoproject.com/>`_

To run some of the prototype services included with the PuppyIR framework (specifically the JuSe prototype):

* `PIL (Python Imaging Library) <http://www.pythonware.com/products/pil/>`_

If you require the use of the 'spelling modifier' (see: :ref:`puppy_spelling_mod` for more on this component) install Enchant:

* `Enchant <http://packages.python.org/pyenchant/>`_

If you require the use of a full text indexer:

* `Whoosh <http://pypi.python.org/pypi/Whoosh/#downloads>`_

If you wish to use the 'SuitabilityFilter' [#f1]_ to filter results and/or make use of Strathclyde University's work in **'trunk/interfaces'** (see :ref:`repo` for more on the structure of the repository) you will need to install Java:

* `Java <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`_  - this site also contains installation instructions for Java.

Basic Installation
------------------

The following sections provide instructions on installing each of the requirements, as detailed in :ref:`basic-requirements-label`.

Install Python
**************

If your system does not have Python installed, or you have an earlier version, you can find the latest 2.7 branch of Python `here <http://python.org/download/>`_. Follow the installation instructions for your own operating system.

At present, Python 3.x is not supported and may cause problems if installed.  You can discover your current version of Python by launching a command prompt and typing the command 'python'.  The version number should be displayed as shown below. If Python 3.0+ is installed, please install the earlier version (the 2.7 branch) to run PuppyIR.

::

  $ python
  Python 2.7.1 (r271:86882M, Nov 30 2010, 10:35:34) 
  [GCC 4.2.1 (Apple Inc. build 5664)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>>

Install Setuptools
******************

This is a pre-requisite to allow several of the other basic dependencies to be installed.

Download the source from http://pypi.python.org/pypi/setuptools

::

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

Install Universal Feed Parser
*****************************

This allows PuppyIR to parse RSS and Atom feeds.

Download the source from http://code.google.com/p/feedparser/

::

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo' 


Install lxml
************

This allows PuppyIR to parse XML files.

Download the source from http://pypi.python.org/pypi/lxml/

:: 

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo' 


Install BeautifulSoup
*********************

This is a HTML/XML parser, one of its main functions is handling tree traversal automatically.

Download the source from http://www.crummy.com/software/BeautifulSoup/#Download

:: 

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

.. _install-puppy-ir:

Installing the PuppyIR Framework
*********************************************

There are two options for installing the PuppyIR framework itself, either you can install the latest development version, or, install a specific release of the framework.

Option 1: Installing a specific release
*********************************************

If you require a specific release, for your application, or simply wish to use a release that is likely to be stable, then choose this option and follow the instructions below.

Download the specific release you want from http://sourceforge.net/projects/puppyir/files/release/ then:

::

  $ cd path/to/puppyir
  $ python setup.py install # may require 'sudo' 

Option 2: Installing the development version
*********************************************

Alternatively, the very latest release - the development version - can be checked out of the repository by following the instructions below:

::

  $ svn export https://puppyir.svn.sourceforge.net/svnroot/puppyir/trunk/framework puppyir
  $ cd puppyir
  $ python setup.py install # may require 'sudo' 

N.B. the development version is not guaranteed to be stable and may be incompatible with certain prototypes and/or demonstrators.

Installing the Extras
---------------------

The following sections, provide instructions on installing each of the extra requirements (as detailed in :ref:`extra-requirements-label`).

Install Django
**************

(Only required if building web services that require or make use of the Django web application framework)

Django is a Python based web framework designed to build web applications quickly, installing this allows developers/researchers to take advantage of the many features offered by Django and also to run the prototypes and demonstrators bundled with the framework.

Download source from https://www.djangoproject.com/download/

::

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

Install Python Imaging Library (PIL)
************************************

(Only required for the JuSe prototype)

This is a library that provides allows various image processing tasks to be done on a large variety of image formats.

Download the source from http://www.pythonware.com/products/pil/

:: 

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

Install Enchant
***************

(Only required if using the 'spelling modifier' - see: :ref:`puppy_spelling_mod` for more on this component)

This is a library that checks the spelling of words and provides a list of suggested correct spellings.

It requires enchant library (version 1.5.0 or greater) which can be downloaded at http://www.abisource.com/projects/enchant/ - installation instructions can be found on this site as well.

Then download Enchant for Python from http://packages.python.org/pyenchant/

:: 

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

Install Whoosh
**************

(Only required for local full text indexing and to run certain prototypes & demonstrators)

Download source from http://pypi.python.org/pypi/Whoosh/#downloads

::

  $ cd /path/to/source
  $ python setup.py install # may require 'sudo'

.. [#f1] For the 'SuitabilityFilter' to work you need to have java added to your system path; how to go about this varies depending on the Operating System (OS) you are using - there are many articles on the internet explaining how to do this for all the major OS's so this is not detailed here.