__author__ = 'mickeypash'
from pyteaser import Summarize
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from blessings import Terminal
import re
import itertools
import os

work_dir = os.getcwd()
my_whoosh_doc_index_dir = '/Users/mickeypash/ifind/applications/treconomics_project3/data/test100index/'

ix = open_dir(my_whoosh_doc_index_dir)

t = Terminal()

with ix.searcher(weighting=scoring.BM25F()) as mysearcher:

    qp = QueryParser("content", ix.schema)
    query_list = ['airport', 'wildlife', 'privacy', 'news']

    for query in itertools.islice(query_list, 0, 10):

        q = qp.parse(unicode('id:1'))
        bm25f = scoring.BM25F()

        matcher = q.matcher(mysearcher)
        bm25f_scorer = bm25f.scorer(mysearcher, 'alltext', query)

        score = bm25f_scorer.score(matcher)
        print query, score

        # myquery = qp.parse(query)
        # results = mysearcher.search(myquery)
        #
        # results.fragmenter.charlimit = None
        #
        # for i, hit in enumerate(itertools.islice(results, 0, 20)):
        #     title = hit["title"]
        #     document = hit["content"]
        #     summaries = Summarize(title, document)
        #
        #     print '%d %s' % (i+1, title.title())
        #     print t.red(re.sub('<[^<]+?>', '', hit.highlights("content")))
