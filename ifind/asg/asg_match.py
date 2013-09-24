__author__ = 'sean'

import random
from asg_generator import YieldGenerator, CueGenerator
from abstract_search_game import ABSGame

class ABSMatch(object):
    def __init__(self, matchlen=3, gametype="3High"):
        self.matchlen = matchlen
        self.gametype = gametype
        self.game_no = 0
        self.games = []
        self.totalpoints = 0

    def start_match(self):
        if self.gametype = "3High":
            self._threeHighGame()

    def end_match(self):
        pass

    def next_game(self):
        if self.is_match_over():
            self.end_match()
        else:
            if self.gametype = "3High":
                self._threeHighGame

    def is_match_over(self):
        if self.game_no > matchlen:
            return True
        else:
           return False

    def _threeHighGame():
        self.game_no += 1
        self.yg = ConstantLinearYieldGenerator()
        self.cg = CueGenerator()
        self.games.append(ABSGame(self.yg, self.cg))

    def get_match_state(self):
        matchdata = {}
        matchdata['totalpoints'] = self.totalpoints
        matchdata['no'] = self.game_no
        matchdata['matchover'] = self.is_game_over()
        return matchdata
