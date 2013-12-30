# challenge 9e-go.py by GM3D ver 0.9
# data: sorted list + dict, lookup: count and bisect
# sorting prices separately.
# sorting cprices.
# adopting lowest price from actual data
# ignoring prices that are larger than any of campaign price.
# finding "exact" solutions first.
# bisect_left <= linear search with hint

import sys

def linear_search(array, value):
    hint = l * (value - lowest_price) / (spread + 1)
    if array[hint] < value:
        for i in xrange(hint, l):
            if array[i] >= value:
                return i
        return l
    else:
        for i in xrange(hint - 1, -1, -1):
            if array[i] < value:
                return i + 1
        return 0

sys.setcheckinterval(1000000)

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
    if larger > highest_price:
        larger = highest_price
    if larger < lowlimit:
        return candidate
    i = linear_search(prices, larger)
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
        smaller = prices[linear_search(prices, smaller) - 1]
        if smaller < lowest_price:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

lines=sys.stdin.read().splitlines()

N, D = map(int, lines[0].split())

cprices = [int(lines[1 + N + day]) for day in xrange(D)]
cp_sorted = sorted(cprices)
maxprice = cp_sorted[D - 1]

prices = [0]
multiplicity = {}

for i in xrange(N):
    price = int(lines[1 + i])
    if price <= maxprice - hard_lowest:
        if price in multiplicity:
            multiplicity[price] += 1
        else:
            multiplicity[price] = 1
            prices.append(price)

prices.sort()
l = len(prices)
lowest_price = prices[1]
highest_price = prices[-1]
spread = highest_price - lowest_price

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
