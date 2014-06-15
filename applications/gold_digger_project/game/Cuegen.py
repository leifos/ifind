from game import Yieldgen

import random


def make_cue(yield_array, scan):
    cue_patterns = 6    # The number of possible cue patterns
    max_gold2 = Yieldgen.b # The maximim number of gold you can get
    cue_range = round(max_gold2/cue_patterns)  # The range of gold represented by a cue
    cue_array = []

    span = round((max_gold2 -(scan*max_gold2))/2)

    print "span"
    print span

    for index in range(len(yield_array)):
        max_gold = max_gold2
        gold = yield_array[index]
        upper_limit = gold+span
        lower_limit = gold-span
        cue = random.randint(lower_limit, upper_limit)
        cueno = 6


        for x in range(cue_patterns):
            if cue < 0:
                cue_array.append(1)
                break
            elif (max_gold+span) >= cue >= max_gold:
                cue_array.append(cueno)
                break
            elif max_gold >= cue >= max_gold-cue_range:
                cue_array.append(cueno)
                break
            elif max_gold < 0:
                cue_array.append(1)
            else:
                max_gold = (max_gold-cue_range)
                cueno-=1



    return cue_array

