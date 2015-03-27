
class Block (object):

    def __init__(self, position, gold, cue):
        """
        Each mine is composed by an array of Block objects

        :param position:
        :param gold:
        :param cue:
        :return:
        """
        self.pos = position
        self.gold = gold
        self.gold_extracted = 0
        self.cue = cue
        self.dug = False

    def __str__(self):
        return 'Block pos: {pos},   gold: {gold},   cue: {cue},    dug: {dug}'.format\
            (pos=self.pos, gold=self.gold, cue=self.cue, dug=self.dug)
