# challenge12.py by GM3D ver 0.1
# based on challenge9.py 
# reading from stdin and storing count_and_offset are changed.
# algorithm is unchanged.

from bisect import bisect_left, insort
from sys import stdin

lowest_price = 10

def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(p_list, larger)
    if not larger in count_and_offset:
        i -= 1
        larger = p_list[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in count_and_offset or \
                (count_and_offset[smaller] == 1 and cp == 2 * larger)):
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

lines=stdin.read().splitlines()

N, D = map(int, lines[0].split())

p_list = [0]
count_and_offset = {0:1}
for i in xrange(N):
    price = int(lines[1 + i].rstrip())
    try:
        count_and_offset[price] += 1
    except KeyError:
        count_and_offset[price] = 1
        insort(p_list, price)

cprices = []
cp_sorted = []
for i in xrange(D):
    price = int(lines[1 + N + i])
    insort(cp_sorted, price)
    cprices.append(price)

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
