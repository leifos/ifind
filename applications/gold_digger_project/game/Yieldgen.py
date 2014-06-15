__author__ = 'gabriele'
import random

m = -4  # m is the slope of the linear function
b = 42  # x is the x value of the linear function


def random_yield(depth):
    random_yield_array = []
    for index in range(depth):
        random_yield_array.append(random.randint(1, 42))
    return random_yield_array


def constant_yield(depth):
    constant_yield_array = []
    yield_constant = random.randint(1,42)
    print "constant"
    print yield_constant
    for index in range(depth):
        constant_yield_array.append(yield_constant)
    return constant_yield_array


def linear_yield(depth):
    linear_yield_array = []
    for index in range(depth):
        linear_yield_array.append(linear_function(index))
    return linear_yield_array


def linear_function(x):
    y = (m*x) + b  # This is the linear yield function
    return y