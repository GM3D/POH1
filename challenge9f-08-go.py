from collections import Counter
import sys

million = int(1e6)
max_days = 50
hard_min_cp = 10
hard_max_cp = million
hard_min_p = 10
hard_max_p = million

def get_next_valid_lower(value):
    if count[value]:
        return value
    else:
        if idx[value]:
            return idx[value]
        else:
            i = value - 1
            d = 0
            while not count[i] and not idx[i]:
                i -= 1
            if count[i]:
                d = i
            if idx[i]:
                d = idx[i]
            idx[i + 1:value + 1] = (value - i) * [d]
            return d

def find_best_price(cp):
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit:
        smaller = cp - larger
        if count[smaller] >= 2:
            return cp
        elif count[smaller] == 1:
            if smaller != larger:
                return cp
        tentative_largers.append(larger)
        larger = get_next_valid_lower(larger - 1)
    candidate = 0
    for larger in tentative_largers:
        smaller = get_next_valid_lower(cp - larger -1)
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

lines = sys.stdin.read().splitlines()
N, D = map(int, lines[0].split())

cprices = [int(lines[1 + N + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)
cp_min = cp_sorted[0]
cp_max = cp_sorted[-1]

count = Counter((int(lines[1 + i]) for i in xrange(N)))
count[0] = 1
lowest_price = min(count.keys())
highest_price = max(count.keys())

idx = [0] * (hard_max_p + 1)

best_prices = [find_best_price(cprices[day]) for day in xrange(D)]

output = "\n".join(map(str, best_prices))
print output
