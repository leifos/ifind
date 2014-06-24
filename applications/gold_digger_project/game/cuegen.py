
import random


cue_patterns = 6


def make_cue(yield_array, scan, max_gold):
    """
    Returns an array of integers representing cue patterns based on an array
    of gold yield, the accuracy of the equipment and the maximum amount of gold

    :param: yield_array
    :param: scan
    :param: max_gold
    :return: cue_array
    """

    cue_range = round(max_gold/cue_patterns)
    cue_array = []
    span = cue_function(scan, max_gold)

    for index in range(len(yield_array)):

        max_gold_yield = max_gold

        gold = yield_array[index]

        upper_limit = gold+span
        lower_limit = gold-span

        cue = random.randint(lower_limit, upper_limit)

        cueno = cue_patterns - 1

        while max_gold_yield >= 0:
            if cue <= 0:
                cue_array.append(0)
                break
            elif (max_gold_yield+span) >= cue >= max_gold_yield and cueno > 0:
                cue_array.append(cueno)
                break
            elif max_gold_yield >= cue >= max_gold_yield-cue_range and cueno > 0:
                cue_array.append(cueno)
                break
            elif max_gold_yield <= 0 or cueno == 0:
                cue_array.append(0)
                break
            else:
                max_gold_yield = (max_gold_yield - cue_range)
                cueno -= 1

    return cue_array


def cue_function(scan, max_gold_yield):
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

    :param: scan
    :param: max_gold_yield
    :return: span
    """
    span = round((max_gold_yield - (scan*max_gold_yield))/2)

    return span
