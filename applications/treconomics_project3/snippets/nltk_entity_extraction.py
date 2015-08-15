__author__ = 'mickeypash'
from nltk import word_tokenize, sent_tokenize
from nltk import ne_chunk_sents
import nltk.data, nltk.tag
tagger = nltk.data.load(nltk.tag._POS_TAGGER)

stop_words = ['Agence France Presse',
              'Associated Press',
              'Central News Agency (Taiwan)',
              'Los Angeles Times-Washington Post',
              'New York Times News Service',
              'Xinhua News Service']


def extract_entities(document):
    # uses NLTK to extract out the Noun Phrases and other meaningful phrases.

    """

    :param document:
    :return:
    """
    sentences = sent_tokenize(document)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [tagger.tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(_extract_entity_names(tree))

    return set(entity_names)


def _extract_entity_names(tree):
    entity_names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'NE':
            tokens = [child[0] for child in tree if child not in stop_words]
            entity_names.append(' '.join(tokens))
        else:
            for child in tree:
                entity_names.extend(_extract_entity_names(child))

    return entity_names