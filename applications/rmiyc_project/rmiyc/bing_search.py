import urllib, urllib2
import json


def run_query(search_terms):
    '''Issues a query to the Bing Search API.
    Args:
        search_terms: is a string containing the query terms
    Returns:
        results: a list where each record is a dict containing: title, link and summary.
    Raises:
        urllib exception
    '''

    # parameters for the search request
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web' # source could be: Image, News, RelatedSearch, Video, or Web
    results_per_page = 10
    offset = 0
    # Bing API expects the query to be in quotes, and quoted! Strange but True.
    query = "'"+ search_terms +"'"
    quoted_query = urllib.quote(query)
    # Construct the URL / search request
    search_url = "%s%s?$format=json&$top=%d&$skip=%d&Query=%s" % (root_url, source, results_per_page, offset, quoted_query)

    # Add the API key to the password manager. There IS no username.
    username = ''
    bing_api_key = "5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ"
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)

    results = []
    try:
        # Prepare an authentication handler and open the URL
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(search_url).read()
        # Convert the response to json and parse out the fields (title, link, and summary)
        json_response = json.loads(response)
        for result in json_response['d']['results']:
            results.append({'title': result['Title'], 'link': result['Url'], 'summary': result['Description']} )

    except urllib2.URLError, e:
        print "Error when querying Bing API", e

    return results