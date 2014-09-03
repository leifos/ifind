__author__ = 'leif'

from ifind.search.query import Query


class SearchContext(object):
    def __init__(self, query_list = []):
        self.query_list = query_list
        self.actions = []
        self.docs_examined = 0
        self.action = None
        self.issued_query_list = []
        self.examined_doc_list = []
        self.query_count = 0
        self.total_docs_examined = 0
        self.total_snippets_examined = 0
        self.snippets_examined = 0
        #TODO(leifos): need to record the position of the current document that is under inspection


    def get_last_action(self):
        if self.actions:
            last_action = self.actions[-1]
        else:
            last_action = None
        return last_action

    def set_snippet_action(self):
        self.action = 'S'
        self.snippets_examined += 1
        self.total_snippets_examined += 1
        self.actions.append(self.action)


    def set_assess_action(self):
        self.action = 'D'
        self.docs_examined += 1
        self.total_docs_examined += 1
        self.actions.append(self.action)


    def set_query_action(self):
        self.action = 'Q'
        self.docs_examined = 0
        self.snippets_examined = 0
        self.actions.append(self.action)





