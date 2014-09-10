__author__ = 'leif'

import random

class DecisionMaker(object):


    def __init__(self, search_interface, search_context):

        self.si = search_interface
        self.sc = search_context

    def decide(self):
        """

        :return: True, if to examine a snippet, False, to issue a query.
        """
        pass


class RandomDecisionMaker(DecisionMaker):

    def __init__(self, search_interface, search_context):
        DecisionMaker.__init__(self, search_interface, search_context)
        self.prob = 0.25

    def decide(self):
        return (random.random() > self.prob)


class FixedDepthDecisionMaker(DecisionMaker):

    def __init__(self, search_interface, search_context):
        DecisionMaker.__init__(self, search_interface, search_context)
        self.depth = 10

    def decide(self):
        return (self.sc.snippets_examined < self.depth)




class SnippetFixedDepthDecisionMaker(DecisionMaker):

    def __init__(self, search_interface, search_context):
        DecisionMaker.__init__(self, search_interface, search_context)
        self.depth = 10
        self.tolerance = 2


    def decide(self):

        if self.sc.snippets_since_last_relevant >= self.tolerance:
            return False
        else:
            return (self.sc.snippets_examined < self.depth)