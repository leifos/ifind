__author__ = 'mickeypash'
from nltk import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk_sents


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