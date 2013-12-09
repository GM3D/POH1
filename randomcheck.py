import random

million = 1000000
l = million * [0]
for i in xrange(million):
    j = random.randrange(million)
    l[j] += 1

non_zero = 0
for i in xrange(million):
    if l[i] != 0:
        non_zero += 1

ratio = (float(non_zero) / million) * 100;
print "%s %% of elements were not zero out of one million." % ratio
