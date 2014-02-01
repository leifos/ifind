__author__ = 'leif'


from abstract_search_game import ABSGame
from asg_generator import RandomYieldGenerator, CueGenerator, ConstantLinearYieldGenerator, TestYieldGenerator
import unittest
import logging
import sys

class TestABSMatch(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestABSMatch")
        self.yg = ConstantLinearYieldGenerator()
        self.cg = CueGenerator()
        self.game = ABSGame(self.yg, self.cg)


class TestABSGame(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestABSGame")
        self.yg = ConstantLinearYieldGenerator()
        self.cg = CueGenerator()
        self.game = ABSGame(self.yg, self.cg)


    def test_query_token(self):
        #self.logger.debug("Test Check Length")
        self.game.issue_query()
        self.game.issue_query()
        self.game.issue_query()
        self.assertEquals(24,self.game.tokens)

    def test_query_token2(self):
        #self.logger.debug("Test Check Length")
        self.game.issue_query()
        self.game.issue_query()
        self.game.issue_query()
        self.game.issue_query()
        self.game.issue_query()
        self.assertEquals(20,self.game.tokens)

    def test_examine_document_no_query(self):
        #self.logger.debug("Test Check Length")
        outcome = self.game.examine_document()
        self.assertEquals(outcome, False)

    def test_examine_document_with_query(self):
        #self.logger.debug("Test Check Length")
        self.game.issue_query()
        outcome = self.game.examine_document()
        self.assertEquals(outcome, True)

        self.assertEquals(self.game.tokens, 27)


    def test_game_token(self):
        self.game.issue_query()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.game.issue_query()
        self.game.examine_document()
        self.game.examine_document()
        self.assertEquals(self.game.tokens,21)


    def test_game_over_given_tokens(self):
        for i in range(14):
            self.game.issue_query()

        outcome = self.game.is_game_over()
        self.assertEquals(outcome, False)

        self.game.issue_query()

        outcome = self.game.is_game_over()
        self.assertEquals(outcome, True)

        outcome = self.game.issue_query()
        self.assertEquals(outcome, False)


    def test_round_generation(self):
        self.game.start_game()
        self.assertEquals(len(self.game.current_round),10)

    def test_rounds(self):
        self.game.start_game()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.assertEquals(self.game.current_round[2]['opened'],True)
        self.assertEquals(self.game.current_round[3]['opened'],False)


    def test_rounds(self):
        self.game.start_game()
        #self.game.print_state()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        #self.game.print_state()
        self.game.issue_query()
        #self.game.print_state()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        #self.game.print_state()

        self.assertEquals(self.game.tokens,20)
        self.assertEquals(self.game.points,8)


class TestTestABSGame(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestABSGame")
        self.yg = TestYieldGenerator()
        self.cg = CueGenerator()
        self.game = ABSGame(self.yg, self.cg)


    def test_game(self):
        self.game.start_game()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.game.examine_document()
        self.game.issue_query()
        self.game.examine_document()
        self.game.examine_document()
        self.game.print_state()
        self.assertEquals(self.game.points,15)
        self.assertEquals(self.game.tokens,22)



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestABSGame").setLevel(logging.DEBUG)
    unittest.main(exit=False)
