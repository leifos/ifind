from gold_digger.logger import event_logger
from block import Block
import cuegen

class Mine(object):

    def __init__(self, yield_generator, scan, user):
        self.blocks = []
        self.yield_generator = yield_generator
        self.depth = self.yield_generator.depth
        self.scan = scan
        self.user = user
        self.make_mine()

    def make_mine(self):
        """
        Generates a Mine with Blocks containing random

        :return: none
        """
        self.blocks = []

        yield_array = self.yield_generator.make_yields()

        yield_array_s = str(yield_array)
        mines_s = str(self.user.mines)
        game_overs = str(self.user.game_overs)
        event_logger.info('USER ' + self.user.user.username + ' LIFE ' + game_overs + ' TOT ' + mines_s + ' MY ' + yield_array_s)
        print "Yield array:", yield_array
        max_gold = 0
        for y in yield_array:
            if y > max_gold:
                max_gold = y



        cue_array = cuegen.make_cue(yield_array, self.scan, max_gold)  # Generate the array of cue values;
        print "Cue array:", cue_array                                                  # based on yield and scanning equipment

        for index in range(self.depth):                              # For every value in the array
            b = Block(index, yield_array[index], cue_array[index])   # Make a block with  yield and cue values
            self.blocks.append(b)                                    # Add the block to the Mine

    def show_mine(self):
        for b in self.blocks:
            print b
