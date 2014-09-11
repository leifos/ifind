__author__ = 'leif'

import random

actions = { 0:'done', 1:'query', 2:'examine_snippet', 3:'examine_document', 4:'mark_document' }



class Screen(object):

    def __init__(self):
        self.actions = []

    def get_data(self):
        return None

class StartScreen(Screen):

    def __init__(self):
        self.actions = [0,1]

class ResultScreen(Screen):

    def __init__(self, snippets):
        self.actions = [0,1,2,3]
        self.snippets = snippets
        self.query = ''

    def get_data(self):
       return self.snippets


class DocScreen(Screen):

    def __init__(self, title, content):
        self.actions = [0,1,4]
        self.title = title
        self.content = content
        self.result_screen = ''

    def get_data(self):
        return (self.title, self.content)


class User(object):

    def __init__(self):
        self.query_list = ['hello','goodbye','ciao']
        self.queries_issued = 0
        self.results_examined = 0
        self.marked_relevant = 0


    def process_topic(self, topic_text):
        """
        User is given a topic and needs to extract out the queries that it could issued
        :param topic_text:
        :return:
        """
        pass


    def select_next_action(self, screen):
        """
        given a screen, calls a method which invokes an action to the driver (experimentor).
        :param Screen:
        :return:
        """

        screen_to_handler = { 'StartScreen': self.handle_start_screen,
                              'ResultScreen': self.handle_result_screen,
                              'DocScreen': self.handle_doc_screen}

        return screen_to_handler[type(screen).__name__](screen)



    def handle_start_screen(self,screen):
        # At the moment, the only action that can be performed on the start screen is to issue a query.
        return self.query()


    def handle_result_screen(self,screen):
        # The user can either issue another query, examine documents or snippets.
        actions = screen.actions
        i = self.results_examined

        # assumes the user always looks at 10 documents
        if i < 10:
            # action to be performed is examine a snippet
            snippet_list = screen.snippets
            # look at snippet in position i
            return self.examine_snippet()

        else:
            return self.query()

    def handle_doc_screen(self,screen):
        # When the view document screen is shown
        pass


    def query(self):
        # select query, or stop
        if self.queries_issued < len(self.query_list):
            query_text = self.query_list[self.queries_issued]
            self.queries_issued = self.queries_issued + 1
            self.results_examined = 0
            return (1, query_text)
        else:
            return (0, None)


    def examine_document(self):
        # look at document, if relevant, mark relevant,
        # then decide to continue to next snippet, or issue new query
        # ASSUMPTION: can we assume that the agent has already compared the document to the topic?
        #             because to get here, the agent must examine the snippet for the document.
        #             or can we say that what is inferred from the snippet in terms of relevance can be different from the actual document?
        document_position = self.results_examined
        document_text = 'some text for the document'
        
        if random.randint(0, 10) > 5: # if the document is relevant to the topic, mark it as relevant.
            self.marked_relevant = self.marked_relevant + 1
            #  Add to a list of marked documents for the given query?
            return (2, snippet_position)
        else:  # Document not considered relevant; so continue
            return (2, None)


    def examine_snippet(self):
        # looks at the next snippet, compare it to the topic,

        snippet_position = self.results_examined
        if random.randint(0,10) > 5:
            # if relevant, then examine document
            return (3, snippet_position)
        else:
            return (2, None)
        # if not, then continue to next snippet or issue new query.









