# challenge 9e.py by GM3D ver 0.2
# data: sorted list + dict, lookup: count and bisect
# sorting prices separately.
# not sorting cprices.
# using self-defined bisect_left

import timeit
import myprofiler
t = myprofiler.ProfileTimer()
t.mark("import")


import sys
from collections import Counter

sys.setcheckinterval(1000000)

def bisect_left(array, value, l):
    i = l / 2
    step = (l + 1) / 4
    while True:
        if i < l and array[i] < value: 
            i += step
        elif i >= 1 and value <= array[i - 1]:
            i -= step
        else:
            break
        if step > 1:
            step /= 2
    return i

t.mark("defs")

lowest_price = 10

def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(prices, larger, l)
    if not larger in multiplicity:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if (not smaller in multiplicity or \
                (multiplicity[smaller] == 1 and cp == 2 * larger)):
            smaller = prices[bisect_left(prices, smaller, l) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = prices[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
            if candidate == cp:
                return candidate
        i -= 1
        larger = prices[i]
    return candidate

t.mark("file input")
lines=sys.stdin.read().splitlines()

t.mark("storing N data into dict")
N, D = map(int, lines[0].split())

t.mark("creating and storing data into list")
prices = [0] + [int(lines[1 + i]) for i in xrange(N)]

t.mark("sorting N data")
prices.sort()
l = len(prices)

t.mark("creating and filling counter")
multiplicity = Counter(prices)
# for i in xrange(N):
#     price = int(lines[1 + i])
#     if price in multiplicity:
#         multiplicity[price] += 1
#     else:
#         multiplicity[price] = 1

prices = [0]
# for i in xrange(N):
#     price = int(lines[1 + i])
#     prices.append(price)
t.mark("main algorithm + output")

cprices = [int(lines[1 + N + day]) for day in xrange(D)]
cp_sorted = sorted(cprices)

best_price = {}
last_best = 1

for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]

t.mark("end")
t.report()
