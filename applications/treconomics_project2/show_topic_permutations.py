__author__ = 'leif'

from ifind.common.rotation_ordering import PermutatedRotationOrdering

topics = ['347', '367', '354', '435']
pro = PermutatedRotationOrdering()

n = pro.number_of_orderings(topics)

for i in range(n):
    print i, pro.get_ordering(topics,i)