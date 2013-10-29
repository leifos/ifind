from whoosh.index import open_dir
import marisa_trie
import operator
import os

#
# Whoosh Trie Test
#

index_path = 'data/smallindex'
vocab_path = 'data/vocab.txt'
stopwords_path = 'data/stopwords.txt'
trie_path = 'data/vocabulary_trie.dat'
min_occurrences = 3


def create_vocab_file():
    """
    Reads the index, creating the vocabulary/frequency text file.
    Returns a handle to the vocabulary file.
    """
    if os.path.exists(vocab_path):
        return open(vocab_path, 'r')
    else:
        vocab_handle = open(vocab_path, 'w+')
        vocab_dict = {}
        stopwords_list = []

        index = open_dir(index_path)
        stopwords_handle = open(stopwords_path, 'r')
        reader = index.reader()

        for word in stopwords_handle:
            stopwords_list.append(word.strip())

        for term in reader.all_terms():
            if term[0] == 'content' or term[0] == 'title':
                term_string = term[1]
                title_frequency = reader.frequency('title', term_string)
                content_frequency = reader.frequency('content', term_string)
                summed_frequency = title_frequency + content_frequency

                if (summed_frequency >= min_occurrences) and (term_string not in stopwords_list):
                    vocab_dict[term_string] = summed_frequency

        index.close()
        vocab_dict = sorted(vocab_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

        for term in vocab_dict:
            vocab_handle.write('{0},{1}{2}'.format(term[0], term[1], os.linesep))

        vocab_handle.seek(0)
        return vocab_handle


def create_trie(vocab_handle):
    """
    Creates and returns a trie from the contents of the file pointed to by the handle vocab_handle
    """
    keys = []
    values = []
    format = '<H'

    for input_line in vocab_handle:
        input_line = input_line.strip()
        input_line = input_line.split(',')

        term = unicode(input_line[0])
        frequency = (float(input_line[1]),)

        keys.append(term)
        values.append(frequency)

    trie = marisa_trie.RecordTrie(format, zip(keys, values))
    return trie


def test_trie(trie, query):
    results = trie.items(u'davi')
    sorted_results =  sorted(results, key=operator.itemgetter(1), reverse=True)
    end_result = [i[0] for i in sorted_results]

    print end_result


def save_trie(trie):
    trie.save(trie_path)

if __name__ == '__main__':
    vocab = create_vocab_file()
    trie = create_trie(vocab)

    test_trie(trie, u"Davi")

    save_trie(trie)