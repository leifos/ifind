import json
import nltk
from nltk.corpus import stopwords, state_union
from nltk.tokenize import word_tokenize, sent_tokenize
from ifind.search import Query, EngineFactory, exceptions
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

    e = EngineFactory("Bing", api_key=BING_API_KEY)

    # A list of SERPs
    result_list = []

    with open(in_filename, "r+") as query_file:
        for item in query_file:
            query = Query(item, top=10)
            results = e.search(query)
            #result_list.append(results)

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


def analyse_snippets(in_filename, out_filename):
    """
        Analyzes  the content of the snippets, length in terms, characters, etc.

    Args:
        file of snippets

    Returns:
        file of snippets features/characteristics
    """
    with open(in_filename, "r+") as fin:
        with open(out_filename, "w") as fout:
            for line in fin:
                characters = len(line)
                words = len(line.split())

                fout.write("C " + str(characters) + " W " + str(words) + "\n")


def reduce_snippets(in_filename, out_filename, percentage=50):
    # Should I reduce TO a percentage or BY a percentage
    """
        Halves their length (or reduces them by whatever percentage) 
    Args: 
        file of snippets, percent reduction
    Returns: 
        listing of snippets
    """
    with open(in_filename, "r+") as fin,\
            open(out_filename, "w+") as fout:
        for snippet in fin:
            word_list = snippet.split()
            word_count = len(word_list)
            percent = percentage / 100.0
            new_len = int(round(word_count * percent))

            new_line = word_list[:new_len]

            fout.write(" ".join(new_line) + "\n")


def remove_stopwords(snippet):
    """

    :param snippet:
    :return: filtered snippet: list of words in snippet excluding stopwords
    """
    words = word_tokenize(snippet)
    stop_words = set(stopwords.words("english"))
    filtered_snippet = [word for word in words if word not in stop_words]

    return filtered_snippet


# preserve the Info Content, by removing stop words
# input: file of snippet, file of stop words (one per file)
# output: listing of snippets

#sample_text = state_union.raw("2006-GWBush.txt")

def extract_entities(snippet_list):
    # uses NLTK to extract out the Noun Phrases and other meaningful phrases.

    try:
        for s in sent_tokenize(snippet_list):
            words = word_tokenize(s)
            tagged = nltk.pos_tag(words)

            named_entity = nltk.ne_chunk(tagged, binary=True)
            named_entity.draw()

    finally:
        pass


# def reduce_snippet():
#
#     # build a list of term frequencies (look at nltk)
#     # if you dont have a background vocabulary, take the top 50 or 100 bing results,
#     # i.e. all the snippets. Then count the number of times each term occurs. Store this in a dict()
#     btc = dict()
#     snippet_list = []
#     for word in snippet_list():
#         btc[word] = frequency_count(word, snippet_list)


def frequency_count(filename):
    """
    Extracts a list of words and their frequencies from a text file (aquaint.txt)
    :param filename:
    """
    btc = dict()
    # with open('filename') as f:
    # lines = f.readlines()

    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines:

        tokens = line.split()
        word = tokens[0]
        frequency = tokens[1]

        btc[word] = int(frequency)

    return btc

def frequency_count2(filename):
    """
    Generates word frequencies from a textfile (snippets.txt)
    :param filename:
    :return:
    """

    file_in = open(filename, "r+")

    wordcount = {}
    for word in file_in.read().split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

    for k, v in wordcount.items():
        print k, v

    file_in.close()


def probs(snippet, term_frequency_file):
    """
        Evaluates the probability of the words in a snippet
        based on term frequencies provided
    :param snippet:
    :return:
    """

    word_counts = frequency_count(term_frequency_file)
    total_word_count = 1.0

    for word in word_tokenize(snippet):
        if not word in word_counts:
            word_counts[word.lower()] = 1
            for i in word_counts:
                word_counts[i] += 1
        total_word_count += word_counts[word]

    word_probs = {}

    for word in word_tokenize(snippet):
        probability = word_counts[word] / total_word_count

        word_probs[word] = probability

    for k, v in word_counts.items():
        print k, v

    for k, v in word_probs.items():
        print k, v
