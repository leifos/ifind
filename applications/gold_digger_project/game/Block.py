__author__ = 'gabriele'
class Block (object):

    def __init__(self, num, gold, cue):
        self.num = num
        self.gold = gold
        self.cue = cue
        self.dug = False


    def __str__(self):
        return 'Block num: {num},   gold: {gold},   cue: {cue},    dug: {dug}'.format\
            (num=self.num, gold=self.gold, cue=self.cue, dug=self.dug)
