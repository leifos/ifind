__author__ = 'mickeypash'
from pyteaser import Summarize
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from blessings import Terminal
import itertools
import os

work_dir = os.getcwd()
my_whoosh_doc_index_dir = '/Users/mickeypash/ifind/applications/treconomics_project3/data/test100index/'

ix = open_dir(my_whoosh_doc_index_dir)

t = Terminal()

parser = QueryParser("content", ix.schema)
myquery = parser.parse('airport')

with ix.searcher() as mysearcher:
    results = mysearcher.search(myquery)
    for i, hit in enumerate(itertools.islice(results, 0, 1)):
        title = hit["title"]
        document = hit["content"]
        summaries = Summarize(title, document)

        print title
        for num, summary in enumerate(summaries):
            with open("summary{0}.txt".format(num), "w+") as fn:
                fn.write(summary)