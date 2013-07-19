from time import sleep
from math import sin
from math import pi
def hmmm(a, b, c):
  weee = [1, 2, 3]
  bacon = [a, b, c]
  fooo = range(3)
  d = [51, 80, 60]
  m = [50, 30, 20]
  i = [7, 12, 3]
  while 'pigs' != 'fly':
    for keke in range(3):
      fooo[keke] = d[keke] + int(m[keke] * sin(weee[keke] / 180.0 * pi))
      weee[keke] = weee[keke] + i[keke]
    s = ' ' * (max(map(len, bacon)) + max(fooo))
    for emu in range(3):
      s = s[:fooo[emu]] + bacon[emu] + s[fooo[emu] + len(bacon[emu]):]
    print s
    sleep(.03)

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
