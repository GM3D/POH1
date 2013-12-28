# challenge10k-go.py ver 0.4
# count_and_offset is list and linearly scanned on demand
# caching search result with index slicing and xrange
# list creation using [0] * repeater

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
        count_and_offset[x - j + 1:x + 1] = xrange(d - 1, d - j - 1, -1)
        return x - j + d

million = 1000 * 1000
max_days = 75
lowest_price = 10

lines=sys.stdin.read().splitlines()

N, D = map(int, lines[0].split())

count_and_offset = [0] * (million + 1)
for i in xrange(N):
    value = int(lines[i + 1])
    count_and_offset[value] += 1

cprices = [int(lines[N + 1 + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)
best_price = {}
last_cp = 0
for i in xrange(D):
    cp = cp_sorted[i]
    if last_cp == cp:
        continue
    last_cp = cp
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

for day in xrange(D):
    print best_price[cprices[day]]
