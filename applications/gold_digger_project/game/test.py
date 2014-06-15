from game import Yieldgen

__author__ = 'gabriele'
import random
a =26
b =34
c = 6

cue_range = []

r = random.randint(a,b)

print r

gold = 30
span = 4
upper_limit = gold+span
lower_limit = gold-span
print upper_limit
print lower_limit

cue = random.randint(lower_limit, upper_limit)

print cue

for x in range(c):
    cue_range.append(a)
    print x

array = Yieldgen.constant_yield(10)

print "Yield array"

for c in array:
    print c

arraycue = Cuegen.make_cue(array, 0.8)

print "arraycue"

for p in arraycue:
    print p



