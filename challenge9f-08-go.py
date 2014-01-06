from bisect import bisect_left
import sys

million = int(1e6)
max_days = 50

def find_best_price(cp):
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_left(prices, larger)
    if not larger in count:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if smaller in count:
            if count[smaller] >= 2:
                return cp
            if count[smaller] == 1 and smaller != larger:
                return cp
        else:
            tentative_largers.append(larger)
        i -= 1
        larger = prices[i]
    candidate = 0
    for larger in tentative_largers:
        i = bisect_left(prices, cp -larger) - 1
        smaller = prices[i]
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

lines = sys.stdin.read().splitlines()
N, D = map(int, lines[0].split())
cprices = [int(lines[1 + N + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)
cp_min = cp_sorted[0]
cp_max = cp_sorted[-1]

count = {0:1}
prices = []
for i in xrange(N):
    price = int(lines[1 + i])
    if price in count:
        count[price] += 1
    else:
        count[price] = 1
        prices.append(price)
prices.sort()
lowest_price = prices[0]
highest_price = prices[-1]
best_prices = [find_best_price(cprices[day]) for day in xrange(D)]
best_ratio = sum([1.0 for i in xrange(D) if best_prices[i] == cprices[i]]) / D
output = "\n".join(map(str, best_prices))
print output
print best_ratio
