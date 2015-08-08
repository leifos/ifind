from __future__ import absolute_import
__author__ = 'mickeypash'
from pyteaser import Summarize
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from blessings import Terminal
from . import nltk_entity_extraction
import itertools
import os

work_dir = os.getcwd()
my_whoosh_doc_index_dir = '../data/test100index/'

ix = open_dir(my_whoosh_doc_index_dir)

t = Terminal()


with ix.searcher(weighting=scoring.TF_IDF()) as mysearcher:

    qp = QueryParser("content", ix.schema)
    query_list = ['airport', 'wildlife', 'privacy', 'news']

    for query in itertools.islice(query_list, 0, 1):

        q = qp.parse(unicode('id:1'))
        bm25f = scoring.TF_IDF()

        matcher = q.matcher(mysearcher)
        bm25f_scorer = bm25f.scorer(mysearcher, 'content', query)

        score = bm25f_scorer.score(matcher)
        # print query, score

        myquery = qp.parse(query)
        results = mysearcher.search(myquery)

        results.fragmenter.charlimit = None

        for i, hit in enumerate(itertools.islice(results, 0, 1)):
            title = hit["title"]
            document = hit["content"]
            summaries = Summarize(title, document)

            # print '%d %s' % (i+1, title.title())
            # print document
            # print t.red(re.sub('<[^<]+?>', '', hit.highlights("content")))
