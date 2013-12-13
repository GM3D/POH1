# challenge10.py by GM3D ver 0.1

from sys import stdin

def get_next_valid_lower(x):
    l = count_and_offset[x]
    if l < 0:
        x += l
    return x

million = 1000 * 1000
max_days = 75
lowest_price = 10

content = stdin.read()
lines=content.splitlines()

N, D = map(int, lines[0].split())

count_and_offset = {}
for i in xrange(N):
    value = int(lines[i + 1])
    try:
        count_and_offset[value] += 1
    except KeyError:
        count_and_offset[value] = 1
        
cprices = map(int, lines[N + 1:])

offset = 0;
for i in xrange(million + 1):
    if i in count_and_offset:
            offset = 0;
    else:
        count_and_offset[i] = offset
    offset -= 1

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
