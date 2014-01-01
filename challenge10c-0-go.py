#challenge10c.py ver 0.0
# count_and_offset is list
# with prescan.
# base pure python impl.
# separete count and itable.
from sys import stdin

million = 1000 * 1000
max_days = 75
hard_lowest = 10

def get_next_valid_lower(x):
    if count[x]:
        return x
    else:
        return idx[x]

def find_best_price(cp):
    candidate = 0
    if cp > 2 * hard_lowest:
        lowlimit = cp / 2
    else:
        lowlimit = hard_lowest
    larger = cp - hard_lowest
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (count[smaller] == 1 and smaller == larger):
            smaller -= 1
        smaller = get_next_valid_lower(smaller)
        if smaller < hard_lowest:
            larger = get_next_valid_lower(larger - 1)
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        larger = get_next_valid_lower(larger - 1)
    return candidate

content = stdin.read()
lines=content.splitlines()
N, D = map(int, lines[0].split())

count = bytearray(million + 1)
idx = [0] * (million + 1)

for i in xrange(N):
    value = int(lines[i + 1])
    count[value] += 1

m = map(int, lines[N + 1:])

o = 0
ilast = 0
for i in xrange(million + 1):
    if count[i] > 0:
        idx[ilast:i] = [o] * (i - ilast)
        o = i
        ilast = i
idx[ilast:million + 1] = [o] * (million + 1 - ilast)

best_price = []
for day in xrange(D):
    best_price.append(find_best_price(m[day]))

for day in xrange(D):
    print best_price[day]
    
    



