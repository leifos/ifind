__author__ = 'gabriele'
import random


def random_yield (depth):
    random_yield_array = []
    for index in range(depth):
        random_yield_array[index] = random.randint(1,10)
    return random_yield_array


def constant_yield(depth, yield_constant):
    constant_yield_array = []
    for index in range(depth):
        constant_yield_array[index] = yield_constant
    return constant_yield_array

def linear_yield(depth):
    linear_yield_array = []
    for index in range(depth)


