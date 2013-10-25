from whoosh.index import open_dir

#
# Whoosh Trie experiment
#

class Node(object):
    '''
    Represents the node of a ternary search tree.
    '''

    def __init__(self, char, is_end):
        self.char = char
        self.is_end = is_end
        self.node_left = None
        self.node_centre = None
        self.node_right = None

class TernaryTree(object):
    '''
    Representation of a ternary tree.
    '''
    def __init__(self):
        self.node_root = None;

    def add(self, word, position=0, param_node=None):
        '''
        Adds a word to the ternary tree.
        '''
        if param_node is None:
            node = Node(word[position], False)

            if self.node_root is None:
                self.node_root = node
        else:
            node = param_node

        if ord(word[position]) < ord(node.char):
            self.add(word, position, node.node_left)
        elif ord(word[position]) > ord(node.char):
            self.add(word, position, node.node_right)
        else:
            if position + 1 == len(word):
                node.is_end = True
            else:
                self.add(word, position + 1, node.node_centre)

    def contains(self, word):
        position = 0
        node = self.node_root

        while node is not None:
            if ord(word[position]) < ord(node.char):
                node = node.node_left
            elif ord(word[position]) > ord(node.char):
                node = node.node_right
            else:
                position += 1

                if position == len(word):
                    return node.is_end

                node = node.node_centre

        return False

def get_vocab_dictionary():
    '''
    Read the vocabulary
    '''
    idx = open_dir('data/smallindex/')
    reader = idx.reader()

    ret_dict = {}

    for obj in reader.all_terms():
        if obj[0] == 'title' or obj[0] == 'content':
            title_freq = reader.frequency('title', obj[1])
            content_freq = reader.frequency('content', obj[1])
            ret_dict[obj[1]] = title_freq + content_freq

    idx.close()
    return ret_dict

def run_script():
    '''
    The main function - run the script.
    '''
    vocab_dict = get_vocab_dictionary()

    tree = TernaryTree()
    print tree.node_root
    tree.add('abc')


if __name__ == '__main__':
    run_script()