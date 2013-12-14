#challenge9b.py
# using multiplicity and sorted price list.

from datetime import datetime, timedelta
t = [datetime.now() for i in range(10)]
from sys import stderr
import cProfile

t[0] = datetime.now()
from bisect import bisect_left, insort
from sys import stdin

lowest_price = 10

t[1] = datetime.now()
def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(prices, larger)
    if not larger in multiplicity:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in multiplicity or \
                (multiplicity[smaller] == 1 and cp == 2 * larger)):
            smaller = prices[bisect_left(prices, smaller) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = prices[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
        larger = prices[i]
    return candidate

t[2] = datetime.now()
lines=stdin.readlines()
header = lines[0].rstrip().split(' ')
N, D = map(int, lines[0].split())
prices = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(lines[1 + i])
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        insort(prices, price)
cprices = []
cp_sorted = []
for i in xrange(D):
    price = int(lines[1 + N + i])
    insort(cp_sorted, price)
    cprices.append(price)

t[3] = datetime.now()
best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

t[4] = datetime.now()
for day in xrange(D):
    print best_price[cprices[day]]

t[5] = datetime.now()
for i in xrange(4):
    stderr.write("t[%d] - t[%d] = %d us.\n" % 
                     (i + 1, i, (t[i + 1] - t[i]).microseconds))
