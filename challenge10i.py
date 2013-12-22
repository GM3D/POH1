#challenge10i.py
# count_and_offset is Counter and linearly scanned on demand
# caching search result.
# data read and parse is unified.

import myprofiler
t = myprofiler.ProfileTimer()

t.mark("start")
from sys import stdin
from collections import Counter

def get_next_valid_lower(x):
    if x in count_and_offset:
        return x
    else:
        j = 0
        while x + j not in count_and_offset and x + j > 0:
            j -= 1
        for k in xrange(-j):
            count_and_offset[x + k] = -k
        return x + j

def read_and_parse(s):
    p = 0
    n = 0
    l = len(s)
    while p < s:
        if s[p] != '\n' and s[p] != ' ':
            n = 10 * n + int(s[p])
        else:
            yield n
            n = 0
        p += 1
    yield n

million = 1000 * 1000
max_days = 75
lowest_price = 10

t.mark("stdin.read()")
content = stdin.read()
#lines=content.splitlines()
data = read_and_parse(content)

N, D = data.next(), data.next()
t.mark("storing N data w try/catch")
count_and_offset = Counter()
count_and_offset[0] = 0
t.mark("store N data with try/catch")
for i in xrange(N):
    count_and_offset[data.next()] += 1
#cprices = map(int, lines[N + 1:])
cprices = [data.next() for i in xrange(D)]

t.mark("precsan (1000001 items)")
# offset = 0;
# for i in xrange(million + 1):
#     if i in count_and_offset:
#             offset = 0;
#     else:
#         count_and_offset[i] = offset
#     offset -= 1

t.mark("search algorithm")
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

t.mark("print result")
for day in xrange(D):
    print best_price[day]
    
t.mark("finish")

t.report()
