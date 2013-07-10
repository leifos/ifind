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

    def _score_rank(self, rank, bonus):
        """
        calculates the score based on the rank of the page
        :param rank: integer
        :return: integer
        """
        print 'bonus'
        print bonus
        if(rank>0):
            top = 10
            x = top+1
            print 'score with no bonus'
            print 100 * (x-rank)

            return bonus + 100 * (x-rank)
        else:
            return 0
