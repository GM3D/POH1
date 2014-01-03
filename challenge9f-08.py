import myprofiler

t = myprofiler.ProfileTimer()
t.mark("import")
from collections import Counter
from bisect import bisect_left
import sys

t.mark("defs")
million = int(1e6)
max_days = 50
hard_min_cp = 10
hard_max_cp = million
hard_min_p = 10
hard_max_p = million

def find_best_price(cp):
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_left(prices, larger)
    if not count[larger]:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if count[smaller] >= 2:
            return cp
        elif count[smaller] == 1:
            if smaller != larger:
                return cp
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

t.mark("read data")
lines = sys.stdin.read().splitlines()
N, D = map(int, lines[0].split())
t.mark("fill cprices")
cprices = [int(lines[1 + N + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)
cp_min = cp_sorted[0]
cp_max = cp_sorted[-1]

t.mark("fill prices count")
count = Counter((int(lines[1 + i]) for i in xrange(N)))
count[0] = 1
prices = sorted(count.keys())
lowest_price = prices[1]
highest_price = prices[-1]

t.mark("create idx table")
idx = [0] * (hard_max_p + 1)

t.mark("main algorithm")
best_prices = [find_best_price(cprices[day]) for day in xrange(D)]

t.mark("output")
output = "\n".join(map(str, best_prices))
print output

t.mark("report")
t.report()
