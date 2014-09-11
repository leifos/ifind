import random
from decision_makers.base_decision_maker import BaseDecisionMaker

class RandomDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Given a probability, returns True or False from decide() dependent upon that probability.
    """
    def __init__(self, search_context):
        super(RandomDecisionMaker, self).__init__(search_context)
        self.__probability = 0.25
    
    def decide(self):
        """
        Returns True or False based upon the probability specified in .__probability.
        """
        return (random.random() > self.__probability)