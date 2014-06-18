__author__ = 'gabriele'
import random

m = -4  # m is the slope of the linear function
b = 42  # b is the y intersect of the function (the maximum number of gold)

class YieldGenerator(object):
    def __init__(self, depth, max=50, min=0):
        self.depth = depth
        self.max = max
        self.min = min


    def make_yields(self):
        pass


class RandomYieldGenerator(YieldGenerator):

    def make_yields(self):
        """ return a list of Blocks with random yields,
         of length equal to depth
        """
        random_yield_array = []
        for index in range(self.depth):
            random_yield_array.append(random.randint(self.min, self.max))

        return random_yield_array


class ConstantYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) of the same number picked at random in a range

        """
        constant_yield_array = []
        yield_constant = random.randint(self.min, self.max)   # Randomly chosen constant in range (0, b)

        for index in range(self.depth):
            constant_yield_array.append(yield_constant)

        return constant_yield_array

class LinearYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a linear function
        (linear_function(x))
        """
        linear_yield_array = []

        for index in range(self.depth):
            linear_yield_array.append(LinearYieldGenerator.linear_function(index))

        return linear_yield_array

    @staticmethod
    def linear_function(x):
        y = (m*x) + b  # This is the linear yield function

        return y