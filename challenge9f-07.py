# challenge 9f.py by GM3D ver 0.7
# data: sorted list + dict, lookup: count and bisect
# incorporating limit value optimizations from challenge9e.py
# data read is peformed by bytearray + generator

from sys import stdin
from bisect import bisect_left, insort

lowest_price = 10
filelen = (200000  + 75) * 8  + 3

def parsegenerator(array):
    p = 0
    n = 0
    while True:
        if array[p] == 10:
            yield n
            n = 0
        else:
            n = n * 10 + array[p] - 48
        p += 1

def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    if larger > highest_price:
        larger = highest_price
    if larger < lowlimit:
        return candidate
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

buf = bytearray(filelen)
size = stdin.readinto(buf)
space = buf.index(' ')
buf[space] = '\n'
buf[size] = '\n'
data = parsegenerator(buf)
N = data.next()
D = data.next()

prices = [0]
multiplicity = {}

for i in xrange(N):
    price = data.next()
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        prices.append(price)

prices.sort()
l = len(prices)
lowest_price = prices[1]
highest_price = prices[-1]

cprices = [data.next() for day in xrange(D)]
cp_sorted = sorted(cprices)
maxprice = cp_sorted[-1]

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if c not in best_price:
        if last_best == 0:
            best_price[c] = 0
        else:
            best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
