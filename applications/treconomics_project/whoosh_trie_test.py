from whoosh.index import open_dir
import marisa_trie
import operator

#
# Whoosh Trie experiment
#

def get_trie():
    '''
    Read the vocabulary, return a trie representation
    '''
    idx = open_dir('data/smallindex/')
    reader = idx.reader()

    ret_dict = {}
    min_occurences = 3

    # get the terms
    # if it occurs > 3? times, save to a file
    # order the words by the number of times they occur
    # add to the trie in that order.

    for obj in reader.all_terms():
        if obj[0] == 'content' or obj[0] == 'title':
            title_freq = reader.frequency('title', obj[1])
            content_freq = reader.frequency('content', obj[1])

            if (title_freq + content_freq) >= min_occurences:
                ret_dict[obj[1]] = (title_freq + content_freq)

    idx.close()

    sorted_words = sorted(ret_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    #print sorted_words

    return marisa_trie.Trie(x[0] for x in sorted_words)

def run_script():
    '''
    The main function - run the script.
    '''
    trie = get_trie()

    print trie.keys(u'sai')

    # stopword removal
    #


if __name__ == '__main__':
    run_script()