#challenge10f.py
# count_and_offset is list
# with prescan.
# other optimizations imported from challenge9e.py

def print_array(array):
    for i in xrange(len(array)):
        if array[i]:
            print "(%d: %d)" % (i, array[i])

import myprofiler
t = myprofiler.ProfileTimer()

t.mark("import")
import sys
def gcd(a, b):
    if(b > a):
        tmp = a
        a = b
        b = tmp
    while True:
        r = a % b
        if not r:
            return b
        else:
            a = b
            b = r

def get_next_valid_lower(x):
    l = count_and_offset[x]
    if l < 0:
        x += l
    return x

million = 1000 * 1000
max_days = 75
hard_lowest = 10

t.mark("file read")

lines=sys.stdin.read().splitlines()

N, D = map(int, lines[0].split())

t.mark("fill cprices and make cp_sorted")
cprices = [int(lines[N + 1 + i]) for i in xrange(D)]
cp_sorted = sorted(cprices)
maxcp = cp_sorted[-1]
denom = cp_sorted[0]
denom = reduce(gcd, cp_sorted, denom)

t.mark("create list of (highest_price + 1) length")
count_and_offset = [0] * (maxcp + 1)

t.mark("count data <= limit only")
lowest_price = million
highest_price = 0
for i in xrange(N):
    value = int(lines[i + 1])
    if value <= maxcp - hard_lowest:
        count_and_offset[value] += 1
    if denom > 1:
        denom = gcd(denom, value)
    lowest_price = min(lowest_price, value)
    highest_price = max(highest_price, value)

# print "real data:"
# print "lowest = %d, highest = %d" % (lowest_price, highest_price)
# print "cprices = ", cprices
# print "cp_sorted =", cp_sorted
# print_array(count_and_offset)
# print "denom = %d" % denom

if denom > 1:
    count_and_offset = [count_and_offset[denom * i] \
                      for i in xrange(maxcp / denom + 1)]
    cprices = [p / denom for p in cprices]
    cp_sorted = [p / denom for p in cp_sorted]
    lowest_price /= denom
    highest_price /= denom
    maxcp /= denom
    
# print "denominated data:"
# print "lowest = %d, highest = %d" % (lowest_price, highest_price)
# print "cprices = ", cprices
# print "cp_sorted =", cp_sorted
# print_array(count_and_offset)
    
t.mark("prescan entries")
offset = 0;
for i in xrange(maxcp + 1):
    if count_and_offset[i] > 0:
            offset = 0;
    else:
        count_and_offset[i] = offset
    offset -= 1

def find_best_price(cp):
#    print "cp =", cp
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
#    print "initial larger =", larger
    if larger < lowlimit:
        return 0
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit:
        smaller = cp - larger
#        print "checking (larger, smaller) = (%d, %d)" % (larger, smaller)
        if count_and_offset[smaller] >= 2:
#            print "(%d, %d) optimal is solution." % (larger, smaller)
            return cp
        elif count_and_offset[smaller] == 1:
            if smaller != larger:
#                print "(%d, %d) is optimal solution." % (larger, smaller)
                return cp
#        print "%d as larger is at best sub-optimal, checking further later." % larger
        tentative_largers.append(larger)
        larger = get_next_valid_lower(larger - 1)

    candidate = 0
    for larger in tentative_largers:
        smaller = get_next_valid_lower(cp - larger -1)
        
        if smaller + larger > candidate:
#            print "suboptimal candidate : (larger, smaller) = (%d, %d)" % (larger, smaller)
            candidate = smaller + larger

    return candidate

t.mark("main algorithm")
best_prices = {}
for day in xrange(D):
    if cprices[day] not in best_prices:
        best_prices[cprices[day]] = find_best_price(cprices[day])

t.mark("print result")
for day in xrange(D):
    print denom * best_prices[cprices[day]]
    
t.mark("report")

t.report()
