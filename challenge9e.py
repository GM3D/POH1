# challenge 9e.py by GM3D ver 0.7
# data: sorted list + dict, lookup: count and bisect
# sorting prices separately.
# sorting cprices.
# adopting lowest price from actual data
# ignoring prices that are larger than any of campaign price.
# finding "exact" solutions first.

import timeit
import myprofiler
t = myprofiler.ProfileTimer()
t.mark("import")


import sys

sys.setcheckinterval(1000000)
#from bisect import bisect_left

def bisect_left(array, value):
    l = len(array)
    for i in xrange(l):
        if array[i] >= value:
            return i
    return l

t.mark("defs")

hard_lowest = 10

def find_best_price(cp):
    tentative_largers = []
    lowest_price = prices[1]
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    if larger < hard_lowest:
        return candidate
    i = bisect_left(prices, larger)
    if not larger in multiplicity:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if smaller in multiplicity and \
                (multiplicity[smaller] == 2 or smaller != larger):
            return cp
        tentative_largers.append(larger)
        i -= 1
        larger = prices[i]
    for larger in tentative_largers:
        smaller = cp - larger
        smaller = prices[bisect_left(prices, smaller) - 1]
        if smaller < lowest_price:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

t.mark("file input")
lines=sys.stdin.read().splitlines()

t.mark("storing N data into dict")
N, D = map(int, lines[0].split())

cprices = [int(lines[1 + N + day]) for day in xrange(D)]
cp_sorted = sorted(cprices)
maxprice = cp_sorted[D - 1]

t.mark("creating and filling dict and list")
multiplicity = {}
prices = [0]

for i in xrange(N):
    price = int(lines[1 + i])
    if price <= maxprice - hard_lowest:
        if price in multiplicity:
            multiplicity[price] += 1
        else:
            multiplicity[price] = 1
            prices.append(price)

t.mark("sorting (maximally) N data")
prices.sort()
l = len(prices)

t.mark("main algorithm + output")

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
