__author__ = 'gabriele'

from game import Block


class Mine(object):

    def __init__(self, depth, mine_type):
        self.blocks = []
        self.depth = depth
        self.mine_type = mine_type


    def make_random_mine(self):
        for index in range(self.depth):  # Create each block of the mine
            b = Block.Block(index+1)     # Each block is numbered
            b.make_random_block()               # Each block is made according to some yield function
            self.blocks.append(b)        # Add each block to the array of blocks of the mine
            print(b)

        return self                      # return the Mine object

    def make_constant_mine(self):
        for index in range(self.depth):
            b = Block.Block(index+1)
            b.make_constant_block()
            self.blocks.append(b)
            print (b)