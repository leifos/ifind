from game import Mine

__author__ = 'gabriele'

r = Mine.Mine(10, 'random', 0.1)
cy = Mine.Mine(10, 'constant', 0.1)
l = Mine.Mine(10, 'linear', 0.1)



print '\n' + "Random yield" + '\n'

for a in r.blocks:
    print a

print '\n' + "Constant yield" + '\n'
for b in cy.blocks:

    print b

print '\n' + "Linear Yield" + '\n'
for c in l.blocks:
    print c
