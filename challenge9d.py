from bisect import bisect_left, insort
from sys import stdin

lowest_price = 10

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

lines=stdin.readlines()
header = lines[0].rstrip().split(' ')
N, D = int(header[0]), int(header[1])
prices = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(lines[1 + i].rstrip())
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        insort(prices, price)
cprices = []
cp_sorted = []
for i in xrange(D):
    price = int(lines[1 + N + i].rstrip())
    insort(cp_sorted, price)
    cprices.append(price)

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
