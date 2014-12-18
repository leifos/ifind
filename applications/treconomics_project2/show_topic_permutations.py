__author__ = 'leif'

from ifind.common.rotation_ordering import PermutatedRotationOrdering

topics = ['347','344','435','546']
pro = PermutatedRotationOrdering()

n = pro.number_of_orderings(topics)

for i in range(n):
    print i, pro.get_ordering(topics,i)