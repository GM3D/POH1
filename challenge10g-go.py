#challenge10g-go.py
# count_and_offset is dict and linearly scanned on demand
# caching search result.
from sys import stdin

def get_next_valid_lower(x):
    if x in count_and_offset:
        if count_and_offset[x] > 0:
            return x
        else:
            return count_and_offset[x] + x
    else:
        j = 1
        while x - j not in count_and_offset and x - j > 0:
            j += 1
        if count_and_offset[x - j] < 0:
            d = count_and_offset[x - j]
        else:
            d = 0
        for k in xrange(1, j + 1):
            count_and_offset[x - j + k] = -k + d
        return x - j + d

million = 1000 * 1000
max_days = 75
lowest_price = 10

content = stdin.read()
lines=content.splitlines()

N, D = map(int, lines[0].split())

count_and_offset = {0:0}
for i in xrange(N):
    value = int(lines[i + 1])
    try:
        count_and_offset[value] += 1
    except KeyError:
        count_and_offset[value] = 1
cprices = map(int, lines[N + 1:])

best_price = []
for day in xrange(D):
    candidate = 0
    cp = cprices[day]
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if smaller in count_and_offset:
            if (count_and_offset[smaller] == 1 and smaller == larger):
                smaller -= 1
        smaller = get_next_valid_lower(smaller)
        if smaller < lowest_price:
            larger = get_next_valid_lower(larger - 1)
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        larger = get_next_valid_lower(larger - 1)
    best_price.append(candidate)

for day in xrange(D):
    print best_price[day]
    
