__author__ = 'arazzouk'
from ifind.models.game_mechanics import GameMechanic
import os
import sys
sys.path.append(os.getcwd())


class RMIYCMechanic(GameMechanic):
    '''
    def __init__(self):
        """
        :return: GameMechanic object
        """
        self.game = None
        self.super().__init__()
    '''

    def _score_rank(self, rank):
        """
        calculates the score based on the rank of the page
        :param rank: integer
        :return: integer
        """
        top = 10
        x = top+1
        score = 100 * (x-rank)
        return score
