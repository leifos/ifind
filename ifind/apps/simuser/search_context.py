__author__ = 'leif'

from ifind.search.query import Query
from search_interface import Document

class SearchContext(object):
    def __init__(self, search_interface, topic, query_list = [] ):
        self.si = search_interface
        self.topic = topic
        self.query_list = query_list
        self.actions = []
        self.action = None

        self.issued_query_list = []
        self.examined_doc_list = []
        self.relevant_doc_list = []

        self.depths = []

        self.query_count = 0
        self.last_query = None
        self.last_results = None

        self.total_docs_examined = 0
        self.docs_examined = 0
        self.docs_not_relevant = 0

        self.total_snippets_examined = 0
        self.snippets_examined = 0

        self.current_document = None
        self.current_snippet = None
        self.current_position = 0


        #TODO(leifos): need to record the position of the current document that is under inspection

    def report(self):
        print "Number of Queries Issued: ", self.query_count
        print "Number of Documents Examined", self.total_docs_examined
        print "Number of Snippets", self.total_snippets_examined
        print "Number of Documents Marked Relevant", len(self.relevant_doc_list)
        print "Depths", self.depths

        rank = 0
        for i in self.relevant_doc_list:
            rank += 1
            print "{0} QO {1} {2} {3} Exp".format(self.topic.id, i, rank, rank)


    def get_last_action(self):
        if self.actions:
            last_action = self.actions[-1]
        else:
            last_action = None
        return last_action


    def get_current_document(self):
        return self.current_document

    def get_current_snippet(self):
        return self.current_snippet


    def add_issued_query(self, query):

        self.issued_query_list.append(query)
        self.last_query = query
        self.last_results = self.last_query.response.results


    def get_next_query(self):

        query_text = None
        if len(self.query_list) > self.query_count:
            query = self.query_list[self.query_count]
            self.query_count += 1
            query_text = query[0]

        return query_text


    def get_last_query(self):
        return self.last_query


    def seen_document_before(self, document):
        """
        checks to see if the document is on the examined_doc_list
        :param document: search_interface.Document
        :return: True if seen before, else False
        """
        if document.docid in self.examined_doc_list:
            return True
        else:
            return False


    def set_action(self, action_name):
        action_mapping = {
            'QUERY': self.set_query_action,
            'SERP': self.set_serp_action,
            'SNIPPET': self.set_snippet_action,
            'DOC': self.set_assess_action,
            'MARK': self.set_mark_action
        }

        if action_mapping[action_name]:
            self.actions.append(action_name)
            action_mapping[action_name]()


    def set_snippet_action(self):
        self.snippets_examined += 1
        self.total_snippets_examined += 1

        rs = self.last_results[self.snippets_examined-1]
        snippet = Document(rs.whooshid, rs.title, rs.summary, rs.docid)
        self.current_snippet = snippet

        # set current_document
        document = self.si.get_document(snippet.id)
        self.current_document = document

    def set_assess_action(self):
        # records the current document as examined
        self.docs_examined += 1
        self.total_docs_examined += 1
        self.examined_doc_list.append(self.current_document.docid)


    def set_query_action(self):
        if self.query_count > 0:
            self.depths.append((self.snippets_examined, self.docs_examined))
        self.docs_examined = 0
        self.docs_not_relevant = 0
        self.snippets_examined = 0
        self.current_position = 0
        self.current_document = None
        self.current_snippet = None



    def set_serp_action(self):
        pass

    def set_mark_action(self):
        # records the current document as relevant.
        pass











