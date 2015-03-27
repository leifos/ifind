from whoosh.index import open_dir
from search_interfaces import Document
from ifind.search.engines.whooshtrecweb import WhooshTrecWeb
from search_interfaces.base_interface import BaseSearchInterface

class WhooshSearchInterface(BaseSearchInterface):
    """
    A search interface making use of the Whoosh indexing library - and the ifind search components.
    """
    def __init__(self, whoosh_index_dir, model=2, implicit_or=True):
        super(WhooshSearchInterface, self).__init__()
        
        self.__index = open_dir(whoosh_index_dir)
        self.__reader = self.__index.reader()
        
        self.__engine = WhooshTrecWeb(whoosh_index_dir=whoosh_index_dir,model=model,implicit_or=implicit_or)
    
    def issue_query(self, query):
        """
        Allows one to issue a query to the underlying search engine. Takes an ifind Query object.
        """
        query.top = 75  # Will never get as low as this!
        response = self.__engine.search(query)
        
        self._last_query = query
        self._last_response = response
        
        return response
    
    def get_document(self, document_id):
        """
        Retrieves a Document object for the given document specified by parameter document_id.
        """
        fields = self.__reader.stored_fields(int(document_id))
        
        title = fields['title']
        content = fields['content']
        document_num = fields['docid']
        document_date = fields['timedate']
        document_source = fields['source']
        
        document = Document(id=document_id, title=title, content=content)
        document.date = document_date
        document.doc_id = document_num
        document.source = document_source
        
        return document
        