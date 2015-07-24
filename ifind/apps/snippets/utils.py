"""
A collection of utilities intended to manipulate document summaries (snippets)
"""
import json
import re
from collections import Counter

from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk_sents
from nltk.corpus import stopwords

from ifind.search import Query, EngineFactory
from keys import BING_API_KEY


def run_queries(filename):
    """
    A wrapper method that takes a file containing queries and saves
    the first snippets for every query to a new file (i.e. snippets.txt)

    :param filename:
    Args:
        filename (str): file of queries (one per line)

    Returns:
        listing of snippets (one per line)

    """

    e = EngineFactory('Bing', api_key=BING_API_KEY)

    # A list of SERPs
    result_list = []

    # TODO fix this function
    with open(filename, 'r+') as query_file:
        for item in query_file:
            query = Query(item)
            results = e.search(query)
            result_list.append(results)

    return result_list


def save_result_list(result_list, out_filename):
    """

    :param result_list: A list of SERPs (a list of results)
    :param out_filename: A JSON representation of the SERPs
    :return:
    """
    with open(out_filename, 'r+') as out_file:
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
    # TODO refactor

    """
    Analyzes  the content of the snippets, length in terms, characters, etc.

    :param out_filename:
    :param in_filename:
    Args:
        file of snippets

    Returns:
        file of snippets features/characteristics
    """
    with open(in_filename, 'r+') as fin:
        with open(out_filename, 'w') as fout:
            for line in fin:
                characters = len(line)
                words = len(line.split())

                fout.write("C " + str(characters) + " W " + str(words) + "\n")


def reduce_snippets(in_filename, out_filename, percentage=50):
    # Should I reduce TO a percentage or BY a percentage
    """
        Halves their length (or reduces them by whatever percentage)
    :param out_filename:
    :param percentage:
    :param in_filename:
    Args:
        file of snippets, percent reduction
    Returns:
        listing of snippets
    """
    with open(in_filename, 'r+') as fin, \
            open(out_filename, 'w+') as fout:
        for snippet in fin:
            word_list = snippet.split()
            word_count = len(word_list)
            percent = percentage / 100.0
            new_len = int(round(word_count * percent))

            new_line = word_list[:new_len]

            fout.write(' '.join(new_line) + '\n')


def remove_stopwords(snippet):
    """

    :param snippet:
    :return: filtered snippet: list of words in snippet excluding stopwords
    """
    # preserve the Info Content, by removing stop words
    # input: file of snippet, file of stop words (one per file)
    # output: listing of snippets
    words = word_tokenize(snippet.lower())
    stop_words = set(stopwords.words('english'))
    filtered_snippet = [word for word in words if word not in stop_words]

    return filtered_snippet


# sample_text = state_union.raw("2006-GWBush.txt")

def extract_entities(document):
    # uses NLTK to extract out the Noun Phrases and other meaningful phrases.

    """

    :param document:
    :return:
    """
    sentences = sent_tokenize(document)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(_extract_entity_names(tree))

    return set(entity_names)


def _extract_entity_names(tree):
    entity_names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                entity_names.extend(_extract_entity_names(child))

    return entity_names


def import_term_frequency(document):
    """
    Extracts a list of words and their frequencies from a text file (aquaint.txt)
    :param document:
    """

    btc = dict([line.split() for line in document.split('\n')])
    return btc


def calc_term_frequency(document):
    """
    Generates word frequencies from a document (snippets.txt)
    :param document:
    :return:
    """

    non_word_and_digit = re.compile('[\W_\d]+')
    word_count = Counter([non_word_and_digit.sub('', word.lower()) for word in sorted(document.split())])

    return word_count


def calc_term_probability(snippet, word_count):
    """
    Evaluates the probability of the words in a snippet
    based on term frequencies provided
    :param word_count:
    :param snippet:
    :return:
    """
    # TODO this version does not produce expected output

    total_word_count = sum(word_count.itervalues())

    print total_word_count

    word_probs = {}

    for word in word_tokenize(snippet):
        probability = word_count[word] / total_word_count

        word_probs[word] = probability

    # for k, v in word_probs.iteritems():
    #    print k, v

    return word_probs


def read_file(filename):
    """

    :param filename:
    :return:
    """
    with open(filename) as f:
        document = f.read()

    return document


def gen_snippet(query_term, document, length=3):
    """
    Generates a snippet given a document
    :param query_term: currently works with ONE query term
    :param document: string representation of a document
    :param length: default length of the snippet is set to 3 sentences
    :return: a string representation of the snippet
    """
    sentences = sent_tokenize(document)
    snippet = [sentence for sentence in sentences if query_term in sentence]
    return ' '.join(snippet[:length])
