# coding=utf-8
import urllib, urllib2
from BeautifulSoup import BeautifulSoup

def new_response(self):
    self.title = 'n/a'
    self.description = 'n/a'
    self.total_results = 0
    self.start_index = 0
    self.items_per_page = 0
    self.query = 'n/a'
    self.items = []
    self.namespaces = { }
    return self

# Insert relevant details for Bing API here.
username = ""
accountKey = 'vBtZEi6MNFOKk0YBlLvVq4ycw+T7cBWZsBkN/CNtpZU='
queryBingFor = "'google fibre'" # REMEMBER: use apostrophes within the string, this is what Bing expects
quoted_query = urllib.quote(queryBingFor)

# Create the API URL
rootURL = "https://api.datamarket.azure.com/Bing/Search/"
searchURL = rootURL + "Web?$format=ATOM&Query=" + quoted_query

# Add the API key to the password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, searchURL,username,accountKey)

# Prepare an authentication handler and open the URL
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
readURL = urllib2.urlopen(searchURL).read()

# Create a DOM tree of the returned XML
#dom = minidom.parse(urllib2.urlopen(searchURL))

# For all the search results in the DOM tree, extract title, URL data by tag name and strip out tags
#r = new_response(Response())

print readURL

soup = BeautifulSoup(readURL)


for x in soup.findAll('entry'):
    a = x.find('d:title').string
    b =  x.find('d:description').string
    c =  x.find('d:url').string