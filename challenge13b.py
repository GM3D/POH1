#challenge13b.py
# using multiplicity and sorted price list.
# using stdin.read().splitlines() for input.

from datetime import datetime, timedelta
t = [datetime.now() for i in range(10)]
from sys import stderr
import cProfile

t[0] = datetime.now()

from sys import stdin
from collections import Counter
lowest_price = 10

def bisect_left(array, value):
    l = len(array)
    i = step = l / 2
    while True:
        if i  < l and array[i] < value:
            i += step
        elif i >= 1 and value <= array[i - 1]:
            i -= step
        else:
            break
        step /= 2
        if step == 0:
            step = 1
    return i

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
lines = stdin.read().splitlines()
N, D = map(int, lines[0].split())
<<<<<<< HEAD
prices = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(lines[1 + i])
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        prices.append(price)
#cprices = []
#cp_sorted = []
# for i in xrange(D):
#    cprices.append(int(input()))
cprices = map(int, lines[1 + N:])

prices.sort()
#cp_sorted = sorted(cprices)
=======

prices = [0] + map(int, lines[1:1 + N])
multiplicity = Counter(prices)
prices.sort()

cprices = map(int, lines[1 + N:])
>>>>>>> kuro

t[3] = datetime.now()
for c in cprices:
    print find_best_price(c)

# t[4] = datetime.now()
# for day in xrange(D):
#     print best_price[cprices[day]]

t[4] = datetime.now()
for i in xrange(4):
    stderr.write("t[%d] - t[%d] = %d us.\n" % 
                     (i + 1, i, (t[i + 1] - t[i]).microseconds))
