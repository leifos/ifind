#author@mtbvc
#20/06/2013
#
# Readme file for installing libraries needed to use utils.py


Using scrapeutils.py and utils.py requires:

- selenium 2.33.0
- phantomJS 1.9
- google chrome driver


###########################

Mac ports have an old version of selenium, which does not work correctly with
PhantomJS, use

$sudo port uninstall py27-selenium

to uninstall the package, do

$easy_install install pip

to install pip and then install selenium using pip

$pip install selenium
or
$pip install selenium==2.33.0

Install yolk to check correct versions of packages with

$pip install yolk

To se packages installed do

$yolk -l

###############################

On mac osx PhantomJS can be installed with homebrew,

or 

binary file downloaded from

http://phantomjs.org/download.html

Copy the binary file bin/phantomjs to /usr/bin
phatnomjs needs to be added to the path

$PATH=$PATH:/usr/bin/phantomjs



##################################

Get google driver from 

https://code.google.com/p/chromedriver/downloads/list

add to the path once dowaded.



