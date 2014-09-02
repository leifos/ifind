__author__ = 'leif'

import random

actions = {00: 'STOP',
           10: 'ISSUE_QUERY',
           20: 'EXAMINE_DOCUMENT',
           21: 'MARK_DOCUMENT',
           22: 'DOCUMENT_NOT_RELEVANT'}

##########
## USER ##
##########
class User(object):
    """

    """
    def __init__(self):
        self.query_list = ['apples', 'oranges', 'bananas']
        self.queries_issued = 0
        self.documents_examined = 0
        self.action_history = []

    def set_driver(self, driver):
        """
        Sets the driver reference.
        """
        self.driver = driver

    def start_interaction(self):
        """
        Entry point for the agent to start their interactions.
        First point is to simply issue a query, I guess there is no other way to go about that
        """
        self.__interact()

    def __interact(self):
        """
        Do the interactions - call the appropriate methods to issue queries/examine documents
        Depending on the responses from the driver
        """
        while True:
            query_screen = self.issue_query()

            if query_screen is None:
                print "NO QUERIES, REMAINING, STAHP"
                break
            else:
                print " > Examine SERP"

                while True:
                    doc_screen = self.examine_document(query_screen.get_data())

                    if doc_screen is None:
                        break
                    else:
                        if random.randint(1, 10) > 5:  # Is the document relevant?
                            print " > DOC JUDGED RELEVANT"
                            print doc_screen.get_data()


    def issue_query(self):
        """
        Action which prompts the user to issue a query to the search engine.
        Receives a response from the simulator driver consisting of a screen.
        """
        if self.queries_issued < len(self.query_list):
            query_text = self.query_list[self.queries_issued]

            print "ISSUING QUERY '{0}' to DRIVER".format(query_text)
            response = self.driver.perform_action((10, query_text))
            self.action_history.append((10, response))

            self.queries_issued = self.queries_issued + 1
            self.documents_examined = 0

            return response
        else:
            self.driver.perform_action((00, None))
            return None

    def examine_document(self, snippet):
        """
        Action to examine a document on a SERP
        """

        if self.documents_examined < len(snippet):
            snippet = snippet[self.documents_examined]
            screen = self.driver.perform_action((20, snippet))
            self.documents_examined = self.documents_examined + 1

            return screen
        else:
            self.driver.perform_action((00, None))
            return None


############
## SCREEN ##
############
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

############
## DRIVER ##
############
class Driver(object):
    """
    Test class to drive the basic simulation
    This is the Experimenter
    """
    def __init__(self, user):
        pass
        # References to the search engine, etc.

    def perform_action(self, action):
        """
        Performs an action. So this is the method that does the "interaction" between the user and their computer.
        Parameter action is a tuple of form (ACTION_TYPE, DATA**)
        Depending on ACTION_TYPE, DATA could be 0, 1 or >1
        """
        if action[0] == 10:  # Query
            return self.process_query(action)
        elif action[0] == 20:  # Look at a document
            return self.examine_document(action)

    def process_query(self, action):
        """
        Process a query - returns a screen object
        """
        query_terms = action[1]
        screen = ResultScreen(['snip1', 'snip2', 'snip3'])
        screen.query = query_terms

        return screen

    def examine_document(self, action):
        """
        Examine a documnent - returns a document screen
        """
        doc = action[1]  # this should have a document ID so we can pull out the correct document text
        screen = DocScreen('doc_title', 'doc_content goes here')

        return screen

#############
## SCREENS ##
#############
class Screen(object):
    def __init__(self):
        self.actions = []

    def get_data(self):
        return None

class StartScreen(Screen):
    def __init__(self):
        self.actions = [00,10]

class ResultScreen(Screen):
    def __init__(self, snippets):
        self.actions = [00,10,20]
        self.snippets = snippets
        self.query = ''

    def get_data(self):
       return self.snippets

class DocScreen(Screen):
    def __init__(self, title, content):
        self.actions = [00,10,21]
        self.title = title
        self.content = content
        self.result_screen = ''

    def get_data(self):
        return (self.title, self.content)

##########
## TEST ##
##########
if __name__ == '__main__':
    user = User()
    driver = Driver(user)
    user.set_driver(driver)

    user.start_interaction()