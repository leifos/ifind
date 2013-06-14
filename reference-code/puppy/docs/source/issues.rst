.. _issues:

Known issues with the PuppyIR framework
==========================================================

This section details known issues with the PuppyIR framework and will be kept up-to-date, as new versions of the framework are released.

Python 2.6 issues
-----------------

In the :ref:`overview` section it was noted that the framework is intended to be used with Python 2.7. The use of Python 2.6 has not been tested thoroughly and, as such, the list below of issues with it is not comprehensive (it is recommenced to switch to Python 2.7 to avoid these and other potential problems):

* The aMuSe prototype does not work, due to a change to the **fractions** library between Python 2.6 and Python 2.7 regarding the valid format(s) of data it can handle.
* Both the **YouTube** and **YouTubeV2** wrappers function, but lose all details of thumbnails in Python 2.6 due to a change in how Atom/Xml feeds are parsed.