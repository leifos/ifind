__author__ = 'gabriele'
import Yieldgen
class Block (object):

    def __init__(self, num):
        self.num = num
        self.gold = 0
        self.cue = 0
        self.dug = False

    def make_random_block(self):
        gold = Yieldgen.random_yield(self)
        self.gold =  gold
        print "This is the gold: %d" % self.gold
        return self

    def make_constant_block(self):



    def __str__(self):
        return 'num: {num}, gold: {gold}, cue: {cue}, dug: {dug}'.format\
            (num=self.num, gold=self.gold, cue=self.cue, dug=self.dug)
