from Block import Block

__author__ = 'gabriele'

class Mine(object):

    def __init__(self, depth, yield_generator, scan):
        self.blocks = []
        self.depth = depth
        #self.mine_type = mine_type
        self.scan = scan
        self.yield_generator = yield_generator
        self.yield_generator.depth = depth
        self.make_mine()

    def make_mine(self):
        """
        Generates a Mine with Blocks containing random quantities of gold in a range
        of 1 to 10.

        :return: none
        """
        self.blocks = []

        yield_array = self.yield_generator.make_yields()

        #cue_array = Cuegen.make_cue(yield_array, self.scan)  # Generate the array of cue values;
                                                            # based on yield and scanning equipment

        for index in range(self.depth):                              # For every value in the array
            b = Block(index, yield_array[index], 0)   # Make a block with  yield and cue values
            self.blocks.append(b)                                          # Add the block to the Mine


    def show_mine(self):
        for b in self.blocks:
            print b
