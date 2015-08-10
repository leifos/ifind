from __future__ import absolute_import
__author__ = 'mickeypash'
from pyteaser import Summarize
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from blessings import Terminal
import itertools
import nltk_entity_extraction as nee
import re
import os

work_dir = os.getcwd()
my_whoosh_doc_index_dir = '../data/test100index/'

ix = open_dir(my_whoosh_doc_index_dir)

t = Terminal()


def print_info(query):
    myquery = qp.parse(query)
    results = mysearcher.search(myquery)

    results.fragmenter.charlimit = None

    for i, hit in enumerate(itertools.islice(results, 0, 1)):
        title = hit["title"]
        document = hit["alltext"]
        nee.extract_entities(document)
        summaries = Summarize(title, document)

        print '%d %s' % (i+1, title.title())
        print hit.highlights("alltext")

        # print document
        # for summary in summaries:
        #     print summary
        # print t.red(re.sub('<[^<]+?>', '', hit.highlights("alltext")))


with ix.searcher(weighting=scoring.TF_IDF()) as mysearcher:

    qp = QueryParser('alltext', ix.schema)
    query_list = ['wildlife', 'airport', 'privacy', 'news']

    for query in query_list[0:1]:

        # q = qp.parse(unicode('id:1'))
        q = qp.parse(query)
        bm25f = scoring.TF_IDF()

        matcher = q.matcher(mysearcher)
        bm25f_scorer = bm25f.scorer(mysearcher, 'alltext', query)

        score = bm25f_scorer.score(matcher)
        print query, score

        print_info(query)
