from game import Yieldgen
import random


cue_patterns = 6                                # The number of possible cue patterns
max_gold_yield = Yieldgen.b                     # The maximum number of gold you can get
cue_range = round(max_gold_yield/cue_patterns)  # The range of gold represented by a cue



def make_cue(yield_array, scan):

    cue_array = []
    span = cue_function(scan)

    for index in range(len(yield_array)):

        max_gold = max_gold_yield
        gold = yield_array[index]
        upper_limit = gold+span
        lower_limit = gold-span
        cue = random.randint(lower_limit, upper_limit)

        cueno = cue_patterns - 1

        for x in range(cue_patterns):
            if cue < 0:
                cue_array.append(0)
                break
            elif (max_gold+span) >= cue >= max_gold:
                cue_array.append(cueno)
                break
            elif max_gold >= cue >= max_gold-cue_range:
                cue_array.append(cueno)
                break
            elif max_gold < 0:
                cue_array.append(0)
            else:
                max_gold = (max_gold - cue_range)
                cueno -= 1

    return cue_array

def cue_function(scan):
    """
    Computes the range in which the cue can be displayed. It is a function of the maximum amount of point
    and the accuracy of the scanning tools.

    Example:

    yield value = 10
    accuracy (span) = 0.8 (80%)
    max_gold_yield = 42

    then:
    6 <= cue <= 14

    since:
    (42 - (0.8*42)/2 = 4    (rounded to the nearest integer)
    """
    span = round((max_gold_yield - (scan*max_gold_yield))/2)

    return span
