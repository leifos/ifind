from whoosh.index import open_dir
from search_interfaces import Document
from ifind.search.engines.trecdummy import TrecDummy
from search_interfaces.base_interface import BaseSearchInterface

class TrecDummySearchInterface(BaseSearchInterface):
    """
    A search interface making use of the Whoosh indexing library - and the ifind search components.
    """
    def __init__(self, input_file):
        super(TrecDummySearchInterface, self).__init__()
        self.__engine = TrecDummy(input_file)
    
    def issue_query(self, query):
        """
        Allows one to issue a query to the underlying search engine. Takes an ifind Query object.
        """
        response = self.__engine.search(query)
        self._last_query = query
        self._last_response = response
        
        return response
    
    def get_document(self, document_id):
        """
        Retrieves a Document object for the given document specified by parameter document_id.
        """
        document = Document(id=document_id, title='Title: {0}'.format(document_id), content='Content: {0}'.format(document_id))
        document.date = '1/1/2000'
        document.doc_id = document_id
        document.source = 'Dummy'
        
        return document
