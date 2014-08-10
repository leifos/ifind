from game import cuegen
from yieldgen import RandomYieldGenerator, ConstantYieldGenerator, LinearYieldGenerator, QuadraticYieldGenerator,ExponentialYieldGenerator, CubicYieldGenerator, CaliforniaQuadraticYieldGenerator, BrazilQuadraticYieldGenerator, YukonQuadraticYieldGenerator, ScotlandQuadraticYieldGenerator, SouthAfricaQuadraticYieldGenerator, VictoriaQuadraticYieldGenerator
from mine import Mine
from gold_digger import logger
import os



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


ryg = CaliforniaQuadraticYieldGenerator(depth=10, max=maxgold, min=0)
cyg = YukonQuadraticYieldGenerator(depth=10, max=maxgold, min=0)
lyg = BrazilQuadraticYieldGenerator(depth=10, max=maxgold, min=0)
qyg = ScotlandQuadraticYieldGenerator(depth=10, max=maxgold, min=0)
eyg = SouthAfricaQuadraticYieldGenerator(depth=10, max=maxgold, min=0)
cuyg = VictoriaQuadraticYieldGenerator(depth=10, max=maxgold, min=0)

logger.event_logger.info("Yield Generators created")

mryg = Mine(ryg, 0.8)
mcyg = Mine(cyg, 0.8)
mlyg = Mine(lyg, 0.8)
mqyg = Mine(qyg, 0.8)
meyg = Mine(eyg, 0.8)
mcuyg = Mine(cuyg, 0.8)

print '\n' + "### Cali ###" + '\n'
mryg.show_mine()

print '\n' + "### Yukon ###" + '\n'
mcyg.show_mine()

print '\n' + "### Brazil ###" + '\n'
mlyg.show_mine()

print '\n' + "### Scotland ###" + '\n'
mqyg.show_mine()

print '\n' + "### SA ###" + '\n'
meyg.show_mine()

print '\n' + "### Victoria ###" + '\n'
mcuyg.show_mine()
