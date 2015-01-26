def reverse(permutations):
    """
    Reverses a list of permutations.
    """
    return permutations[::-1]

def split(permutations):
    """
    Given a list of permutations, returns the first half of the list.
    """
    return permutations[:len(permutations)/2]

def interleave(permutations):
    """
    Given a list of permutations, interleaves the permutations and returns them.
    E.g. [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10] yields [Q1,Q10,Q2,Q9]....
    """
    l1 = permutations[:len(permutations)/2]
    l2 = permutations[len(permutations)/2:][::-1]
    
    return [val for pair in zip(l1, l2) for val in pair]