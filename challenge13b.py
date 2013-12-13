#challenge9b.py
# using multiplicity and sorted price list.

from datetime import datetime, timedelta
t = [datetime.now() for i in range(10)]
from sys import stderr
import cProfile

t[0] = datetime.now()

lowest_price = 10

def bisect_left(array, value):
    l = len(array)
    i = step = l / 2
    while True:
        if i  < l and array[i] < value:
            i += step
        elif i >= 1 and value <= array[i - 1]:
            i -= step
        else:
            break
        step /= 2
        if step == 0:
            step = 1
    return i

t[1] = datetime.now()
def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(p_list, larger)
    if not larger in multiplicity:
        i -= 1
        larger = p_list[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in multiplicity or \
                (multiplicity[smaller] == 1 and cp == 2 * larger)):
            smaller = p_list[bisect_left(p_list, smaller) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = p_list[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
        larger = p_list[i]
    return candidate

t[2] = datetime.now()
N, D = map(int, raw_input().rstrip().split())
p_list = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(input())
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        p_list.append(price)
#cprices = []
#cp_sorted = []
# for i in xrange(D):
#    cprices.append(int(input()))
cprices = (int(input()) for day in xrange(D))

p_list.sort()
#cp_sorted = sorted(cprices)

t[3] = datetime.now()
best_price = {}
for c in cprices:
    print find_best_price(c)

# t[4] = datetime.now()
# for day in xrange(D):
#     print best_price[cprices[day]]

t[4] = datetime.now()
for i in xrange(4):
    stderr.write("t[%d] - t[%d] = %d us.\n" % 
                     (i + 1, i, (t[i + 1] - t[i]).microseconds))
