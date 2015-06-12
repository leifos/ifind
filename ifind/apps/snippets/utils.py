import json
import urllib
import urllib2
from nltk.corpus import stopwords
from keys import BING_API_KEY


def run_queries(in_filename):
    """
        A wrapper method that takes a file containing queries and saves
        the first snippets for every query to a new file (i.e. snippets.txt)

    Args:
        filename (str): file of queries (one per line)

    Returns:
        listing of snippets (one per line)

    """

    result_list = []

    with open(in_filename, "r+") as query_file:
        for query in query_file:
            result = run_query(query)
            result_list.append(result)

    return result_list


def save_result_list(result_list, out_filename):
    """

    :param result_list: A list of SERPs (a list of results)
    :param out_filename: A JSON representation of the SERPs
    :return:
    """
    with open(out_filename, "r+") as out_file:
        for serp in result_list:
            json_results = format_results(serp)
            out_file.write(json_results)


def format_results(results):
    """
        Formats results into JSON
    :param results:
    :return:
    """
    new_format = json.dumps(results, indent=0)

    return new_format


def run_query(search_terms):
    """
        Interfaces with the BING API
    
    Args:
        search_terms (str): query words, phrases or a sentence

    Returns:
        snippet (str): returns the first snippet for a set search_terms

        could also return a list of snippets

    """

    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''

    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # Create our results list which we'll populate.
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)

        # Loop through each page returned, populating out results list.
        # for result in json_response['d']['results']:
        # s = result['Description'].encode("ascii", "ignore")
        # snippets.append(s)
        rank = 1
        for result in json_response['d']['results']:
            results.append({
                'query': search_terms,
                'rank': rank,
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})
            rank += 1

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e

    # Return the list of results to the calling function.
    # print type(snippets[0])
    return results


def analyse_snippets(filename):
    """
        Analyzes  the content of the snippets, length in terms, characters, etc.

    Args:
        file of snippets

    Returns:
        file of snippets features/characteristics
    """
    with open(filename, "r+") as fin:
        with open("features.txt", "w") as fout:
            for line in fin:
                characters = len(line)
                words = len(line.split())

                fout.write("C " + str(characters) + " W " + str(words) + "\n")


def reduce_snippets(percentage=50):
    # Should I reduce TO a percentage or BY a percentage
    """
        Halves their length (or reduces them by whatever percentage) 
    Args: 
        file of snippets, percent reduction
    Returns: 
        listing of snippets
    """
    with open("snippets.txt", "r+") as fin,\
            open("snippets-halved.txt", "w+") as fout:
        for snippet in fin:
            word_list = snippet.split()
            word_count = len(word_list)
            percent = percentage / 100.0
            new_len = int(round(word_count * percent))

            new_line = word_list[:new_len]

            fout.write(" ".join(new_line) + "\n")


def remove_stop_words():
    stop = stopwords.words('english')
    sentence = "this is a foo bar sentence"
    print [i for i in sentence.split() if i not in stop]


# preserve the Info Content, by removing stop words
# input: file of snippet, file of stop words (one per file)
# output: listing of snippets 

def extract_entities():
    pass

# uses NLTK to extract out the Noun Phrases and other meaningful phrases.
