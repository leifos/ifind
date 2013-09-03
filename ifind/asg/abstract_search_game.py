__author__ = 'leif'

import random
from asg_generator import YieldGenerator, CueGenerator


class ABSGame(object):

    def __init__(self, yield_generator, cue_generator, tokens=30, cq=2, ca=1, points=0, round_len = 10, id=0):
        self.ygen = yield_generator
        self.cgen = cue_generator
        self.tokens = tokens
        self.tokens_spent = 0
        self.cq = cq
        self.ca = ca
        self.current_round = None
        self.round_len = round_len
        self.points = points
        self.round_no = 0
        self.id=id
        self.docs_assessed = 0
        self.queries_issued = 0

    def start_game(self):
        self._make_round()

    def issue_query(self):
        """
        """
        if self.tokens - self.cq >= 0:
            self.tokens = self.tokens - self.cq
            self.tokens_spent = self.tokens_spent + self.cq
            self._make_round()
            self.queries_issued = self.queries_issued + 1
            return True
        else:
            return False


    def examine_document(self):
        if self.round_no == 0:
            return False

        if (self.tokens - self.ca >=0):
            self.tokens = self.tokens - self.ca
            self.tokens_spent = self.tokens_spent + self.ca
            # modify the current_round data
            self.docs_assessed = self.docs_assessed + 1

            # update the round - by opening the first unopened document
            gain = self._open_document()

            # update points with any gain recieved.
            self.points = self.points +  gain

            return True
        else:
            return False


    def end_game(self):
        pass

    def is_game_over(self):
        if self.tokens <= 0:
            return True
        else:
            return False


    def _make_round(self):
        """
        :return: returns a list of dicts (containing label, yield, opened)
        """

        self.round_no += 1
        yl = self.ygen.get_yields(self.round_len)
        print 'cu'
        cl = self.cgen.get_labels(self.round_len, yl)

        rl = []
        for i in range(self.round_len):
            rl.append(self._make_snippet(cl[i],yl[i],False))

        self.current_round = rl

    def _make_snippet(self, label, gain, opened):
        """
        :param label: string
        :param gain: integer
        :param opened: boolean
        :return: dictionary of these attributes
        """

        return {'label': label, 'gain':gain, 'opened': opened }


    def _open_document(self):

        for i in range(self.round_len):
            r = self.current_round[i]
            if not r['opened']:
               r['opened'] = True
               return r['gain']

        return 0


    def get_state(self):
        """
        :return: a dict composed of the game state attributes and round data
        """
        pass

    def print_state(self):
        print "Number of Tokens: %d" % (self.tokens)
        print "Points: %d" % (self.points)
        print "Query Cost: %d Assessment Cost %s" % (self.cq, self.ca)
        if self.current_round:
            for i in self.current_round:
                print i



    def get_game_state(self):
        data = {}
        data['tokens'] = self.tokens
        data['cq'] = self.cq
        data['ca'] = self.ca
        data['points'] = self.points
        data['round'] = self.current_round
        data['no'] = self.round_no
        data['gameover'] = self.is_game_over()
        return data








