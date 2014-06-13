__author__ = 'gabriele'
import Yieldgen

class Mine(object):

    def __init__(self, depth, mine_type):
        self.blocks = []
        self.depth = depth
        self.mine_type = mine_type

        if mine_type == 'random':
            print 'random'
        elif mine_type == 'constant':
            print 'constant'
        elif mine_type == 'linear':
            print 'linear'