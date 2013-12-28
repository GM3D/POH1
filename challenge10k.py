# challenge10k.py
# count_and_offset is list and linearly scanned on demand
# caching search result with index slicing.


import myprofiler
t = myprofiler.ProfileTimer()

t.mark("start")
import sys

def get_next_valid_lower(x):
    if count_and_offset[x] > 0:
        return x
    elif count_and_offset[x] < 0:
        return count_and_offset[x] + x
    else:
        j = 1
        while count_and_offset[x - j] == 0 and x - j > 0:
            j += 1
        if count_and_offset[x - j] < 0:
            d = count_and_offset[x - j]
        else:
            d = 0
        count_and_offset[x - j + 1:x + 1] = range(d - 1, d - j - 1, -1)
        return x - j + d

million = 1000 * 1000
max_days = 75
lowest_price = 10

t.mark("input")
lines=sys.stdin.read().splitlines()

N, D = map(int, lines[0].split())

t.mark("creating list with million 0's")
count_and_offset = [0] * (million + 1)

t.mark("storing N data")
for i in xrange(N):
    value = int(lines[i + 1])
    count_and_offset[value] += 1

t.mark("creating cprices and cp_sorted")
cprices = [int(lines[N + 1 + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)

t.mark("search algorithm")
best_price = {}

for i in xrange(D):
    cp = cp_sorted[i]
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if count_and_offset[smaller] == 0 or \
                (count_and_offset[smaller] == 1 and smaller == larger):
            smaller -= 1
        smaller = get_next_valid_lower(smaller)
        if smaller < lowest_price:
            larger = get_next_valid_lower(larger - 1)
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        larger = get_next_valid_lower(larger - 1)
    best_price[cp] = candidate

t.mark("print result")
for day in xrange(D):
    print best_price[cprices[day]]
    
t.mark("finish")

t.report()
