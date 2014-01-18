import random

million = int(1e6)

s0 = 0
for i in xrange(million):
    x = random.randrange(10, million)
    s = str(x)
    s0 += len(s)

print float(s0) / million

#result: 5.889039
