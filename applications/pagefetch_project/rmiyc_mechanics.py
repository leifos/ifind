__author__ = 'arazzouk'
from ifind.models.game_mechanics import GameMechanic
import os
import sys
import math
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

    def is_game_over(self):
        return self.game_over


    def _score_rank(self, rank, bonus ,query_len=1):
        """
        calculates the score based on the rank of the page
        :param rank: integer
        :return: integer
        """


        if(rank>0):
            top = 10
            x = top+1
            #return bonus + 100 * (x-rank)
            score = 100 * (x-rank) * self.f(query_len)
            return int(score)
        else:
            return 0

    def f(self, query_len):
        return 1/ (math.pow(query_len,0.3))