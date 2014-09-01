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


    def process_topic(self, topic_text):
        """
        User is given a topic and needs to extract out the queries that it could issued
        :param topic_text:
        :return:
        """
        pass


    def select_next_action(self, screen):
        """
        given a
        :param Screen:
        :return:
        """

        screen_to_handler = { 'StartScreen': self.handle_start_screen,
                              'ResultScreen': self.handle_result_screen,
                              'DocScreen': self.handle_doc_screen}

        return screen_to_handler[type(screen).__name__](screen)



    def handle_start_screen(self,screen):

        return self.query()


    def handle_result_screen(self,screen):

        actions = screen.actions
        i = self.results_examined

        # assumes the user always looks at 10 documents
        if i < 10:
            # action to be performed is examine a snippet
            snippet_list = screen.snippets
            # look at snippet in position i

            if random.randint(0,10) > 5:
                return self.examine_snippet()
            else:
                return self.examine_document()
            # if snippet looks relevant, examine document

        else:
            return self.query()



    def handle_doc_screen(self,screen):
        pass


    def query(self):
        # pick off the first query
        query_text = ''
        if self.queries_issued < len(self.query_list):
            query_text = self.query_list[self.queries_issued]
            self.queries_issued = self.queries_issued + 1
            self.results_examined = 0
            return (1, query_text)
        else:
            return (4, None)


    def examine_document(self):
        pass


    def examine_snippet(self):
        pass








