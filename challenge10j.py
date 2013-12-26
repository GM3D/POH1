#challenge10j.py
# count_and_offset is dict and linearly scanned on demand
# caching search result.


import myprofiler
t = myprofiler.ProfileTimer()

t.mark("start")
from sys import stdin

def get_next_valid_lower(x):
    print "get_next_valid_lower: x =", x
    if count_and_offset[x] > 0:
        print "found x in data, return", x
        return x
    elif count_and_offset[x] < 0:
        print "found x offset to real value, return", count_and_offset[x] + x
        return count_and_offset[x] + x
    else:
        print "x not in data, regsitering."
        j = 1
        while count_and_offset[x - j] == 0 and x - j > 0:
            j += 1
        print "found %d in data (value %d)" % (x - j, count_and_offset[x - j])
        if count_and_offset[x - j] < 0:
            d = count_and_offset[x - j]
        else:
            d = 0
        for k in xrange(1, j + 1):
            count_and_offset[x - j + k] = -k + d
        print "registered x: return", x - j + d
        return x - j + d

million = 1000 * 1000
max_days = 75
lowest_price = 10

t.mark("stdin.read() + splitlines()")
content = stdin.read()
lines=content.splitlines()

N, D = map(int, lines[0].split())

t.mark("create dict with million entries")
#count_and_offset = dict.fromkeys(xrange(million + 1), 0)
count_and_offset = [0 for i in xrange(million + 1)]
t.mark("store N data into dict")
for i in xrange(N):
    value = int(lines[i + 1])
    count_and_offset[value] += 1

cprices = map(int, lines[N + 1:])

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
#    print "cp = ", cp
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit and candidate != cp:
#        print "larger = ", larger
        smaller = cp - larger
        if smaller in count_and_offset:
            if (count_and_offset[smaller] == 1 and smaller == larger):
                smaller -= 1
        smaller = get_next_valid_lower(smaller)
        if smaller < lowest_price:
            larger = get_next_valid_lower(larger - 1)
            continue
#        print "smaller = ", smaller
#        print "smaller + larger = %d, candidate = %d" % (smaller + larger, candidate)
        if smaller + larger > candidate:
            candidate = smaller + larger
#            print "new candidate =", candidate
        larger = get_next_valid_lower(larger - 1)
    best_price.append(candidate)

t.mark("print result")
for day in xrange(D):
    print best_price[day]
    
t.mark("finish")

t.report()
