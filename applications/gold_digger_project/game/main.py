from game import Mine, Cuegen, Yieldgen

__author__ = 'gabriele'

r = Mine.Mine(10, 'random', 0.1)
cy = Mine.Mine(10, 'constant', 0.9)
l = Mine.Mine(10, 'linear', 0.1)

x = Cuegen.cue_range
max = Yieldgen.b

scan = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
sa = []


for s in scan:
    span = Cuegen.cue_function(s)
    sa.append(span)

print ' Accuracy: 90%: {0}  80%: {1},  70%: {2},  60%: {3},  50%: {4},  40%: {5},  30%: {6},  20%: {7}'.format(sa[0], sa[1], sa[2], sa[3], sa[4], sa[5], sa[6], sa[7] )


index = 0
countcue = 5
for d in range(max, 0, -1):
    print d
    index += 1
    if index == x:
        print "^^^^^^^^^^^^^^^^^^^^ Cue ", countcue
        countcue-= 1
        index = 0





print '\n' + "### Random yield ###" + '\n'

for a in r.blocks:
    print a

print '\n' + "### Constant yield ###" + '\n'
for b in cy.blocks:

    print b

print '\n' + "### Linear Yield ###" + '\n'
for c in l.blocks:
    print c

