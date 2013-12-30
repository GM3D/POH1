# challenge 9f.py by GM3D ver 0.6
# data: sorted list + bytearray, lookup: count and bisect
# incorporating limit value optimizations from challenge9e.py
# searching optimal solutions first.
# dict lookup by try-except


from sys import stdin
from bisect import bisect_left

hard_lowest = 10

def find_best_price(cp):
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_left(prices, larger)
    if not multiplicity[larger]:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        count = multiplicity[smaller]
        if count  >= 2:
            return cp
        elif count  == 1:
            if smaller != larger:
                return cp

        tentative_largers.append(larger)
        i -= 1
        larger = prices[i]

    candidate = 0
    for larger in tentative_largers:
        smaller = cp - larger
        smaller = prices[bisect_left(prices, smaller) - 1]
        if smaller < lowest_price:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

lines=stdin.read().splitlines()
N, D = map(int, lines[0].split())

cprices = [int(lines[1 + N + day]) for day in xrange(D)]
cp_sorted = sorted(cprices)
maxprice = cp_sorted[- 1]

prices = [0]
multiplicity = bytearray(maxprice - hard_lowest + 1)

for i in xrange(N):
    price = int(lines[1 + i])
    if price <= maxprice - hard_lowest:
        x = multiplicity[price]
        if x == 0:
            multiplicity[price] += 1
            prices.append(price)
        elif x == 1:
            multiplicity[price] += 1

prices.sort()
l = len(prices)
lowest_price = prices[1]
highest_price = prices[-1]


best_price = {}
last_best = 1
counter0 = counter1 = 0
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]

