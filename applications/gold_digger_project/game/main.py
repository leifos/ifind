from game import cuegen, yieldgen
from yieldgen import RandomYieldGenerator, ConstantYieldGenerator, LinearYieldGenerator
from mine import Mine
import yieldgen

maxgold = 42


scan = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
sa = []


for s in scan:
    span = cuegen.cue_function(s, maxgold)
    sa.append(span)

print '\n' + 'Accuracy: 90%: {0}  80%: {1},  70%: {2},  60%: {3},  50%: {4},  40%: {5},  30%: {6},  20%: {7}'.format(sa[0], sa[1], sa[2], sa[3], sa[4], sa[5], sa[6], sa[7]) + '\n'


index = 0
countcue = 5
x = maxgold/cuegen.cue_patterns
for d in range(maxgold, 0, -1):
    print d
    index += 1
    if index == x:
        print "^^^^^^^^^^^^^^^^^^^^ Cue ", countcue
        countcue-= 1
        index = 0


ryg = RandomYieldGenerator(depth=10, max=maxgold, min=0)
cyg = ConstantYieldGenerator(depth=10, max=maxgold, min=0)
lyg = LinearYieldGenerator(depth=10, max=maxgold, min=0)

m = Mine(ryg, 0.8)
m2 = Mine(cyg, 0.8)
m3 = Mine(lyg, 0.8)

print '\n' + "### Random yield ###" + '\n'
m.show_mine()

print '\n' + "### Constant yield ###" + '\n'
m2.show_mine()

print '\n' + "### Linear Yield ###" + '\n'
m3.show_mine()
