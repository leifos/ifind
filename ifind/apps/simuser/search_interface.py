__author__ = 'leif'

from ifind.search.engine import Engine, EngineFactory
from ifind.search.engines.whooshtrecnews import WhooshTrecNews
from whoosh.index import open_dir

class Document(object):
    def __init__(self, id, title=None, content=None):
        self.id = id
        self.title = title
        self.content = content
        self.docid = id


    def __str__(self):
        return "id: {0} title: {1} content: {2}".format(self.id, self.title, self.content)


class Topic(Document):
    def read_topic_from_file(self, topic_filename):

        first_line = None
        topic_text = ''
        if topic_filename:
            f = open(topic_filename, 'r')
            for line in f:
                if not first_line:
                    first_line = line
                topic_text+= ' ' + line
        self.title = first_line
        self.content = topic_text





class SearchInterface(object):

    def __init__(self):
        self.last_response = None
        self.last_query = None

    def issue_query(self, query):
        """

        :param ifind.search.query:
        :return: ifind.search.response
        """
        pass

    def get_document(self, doc_ref):
        pass


class WhooshInterface(SearchInterface):
    """
    provides a common interface to the search engine and the documents
    """

    def __init__(self, whoosh_dir):
        self.last_response = None
        self.last_query = None

        self.ix = open_dir(whoosh_dir)
        self.ixr = self.ix.reader()

        self.engine = WhooshTrecNews(whoosh_index_dir=whoosh_dir, implicit_or=True)


    def issue_query(self, query):
        """

        :param ifind.search.query:
        :return: ifind.search.response
        """

        response = self.engine.search(query)
        self.last_query = query
        self.last_response = response

        return response

    def get_document(self, doc_ref):

        fields = self.ixr.stored_fields(int(doc_ref))
        title = fields["title"]
        content = fields["content"]
        docnum = fields["docid"]
        doc_date = fields["timedate"]
        doc_source = fields["source"]
        d = Document(id=doc_ref,title=title,content=content)
        d.date = doc_date
        d.docid = docnum
        d.source = doc_source

        return d

