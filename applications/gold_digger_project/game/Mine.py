__author__ = 'gabriele'

from game import Block


class Mine(object):

    def __init__(self, depth):
        self.blocks = []
        self.depth = depth

    def make_mine(self):
        for index in range(self.depth):  # Create each block of the mine
            b = Block.Block(index+1)     # Each block is numbered
            b.make_block()               # Each block is made according to some yield function
            self.blocks.append(b)        # Add each block to the array of blocks of the mine
            print(b.gold)
        return self                      # return the Mine object

