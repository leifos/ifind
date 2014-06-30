from game import cuegen
from yieldgen import RandomYieldGenerator, ConstantYieldGenerator, LinearYieldGenerator, QuadraticYieldGenerator,ExponentialYieldGenerator, CubicYieldGenerator
from mine import Mine
from gold_digger import logger



maxgold = 42


scan = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
sa = []


for s in scan:
    span = cuegen.cue_function(s, maxgold)
    sa.append(span)

print '\n' + 'Accuracy: 90%: {0}  80%: {1},  70%: {2},  60%: {3},  50%: {4},  40%: {5},  30%: {6},  20%: {7}'.format\
    (sa[0], sa[1], sa[2], sa[3], sa[4], sa[5], sa[6], sa[7]) + '\n'


index = 0
countcue = 5
x = maxgold/cuegen.cue_patterns
for d in range(maxgold, 0, -1):
    print d
    index += 1
    if index == x:
        print "^^^^^^^^^^^^^^^^^^^^ Cue ", countcue
        countcue -= 1
        index = 0


ryg = RandomYieldGenerator(depth=10, max=maxgold, min=0)
cyg = ConstantYieldGenerator(depth=10, max=maxgold, min=0)
lyg = LinearYieldGenerator(depth=10, max=maxgold, min=0)
qyg = QuadraticYieldGenerator(depth=10, max=maxgold, min=0)
eyg = ExponentialYieldGenerator(depth=10, max=maxgold, min=0)
cuyg = CubicYieldGenerator(depth=10, max=maxgold, min=0)

event_logger.info("an info message")

mryg = Mine(ryg, 0.8)
mcyg = Mine(cyg, 0.8)
mlyg = Mine(lyg, 0.8)
mqyg = Mine(qyg, 0.8)
meyg = Mine(eyg, 0.8)
mcuyg = Mine(cuyg, 0.8)

print '\n' + "### Random yield ###" + '\n'
mryg.show_mine()

print '\n' + "### Constant yield ###" + '\n'
mcyg.show_mine()

print '\n' + "### Linear Yield ###" + '\n'
mlyg.show_mine()

print '\n' + "### Quadratic Yield ###" + '\n'
mqyg.show_mine()

print '\n' + "### Exponential Yield ###" + '\n'
meyg.show_mine()

print '\n' + "### Cubic Yield ###" + '\n'
mcuyg.show_mine()
