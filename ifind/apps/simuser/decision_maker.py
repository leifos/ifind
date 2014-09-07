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
        self.depth = 20

    def decide(self):
        return (self.sc.snippets_examined < self.depth)


