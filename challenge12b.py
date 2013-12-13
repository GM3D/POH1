# challenge12b.py
# based on challenge9.py 
# reading from stdin and storing count_and_offset are changed.
# algorithm is unchanged.

from datetime import datetime, timedelta
from sys import stderr

num_marks = 10
def report_time():
    for i in xrange(num_marks - 1):
        if t[i+1] > t[i]:
            stderr.write("t[%d] - t[%d] = %d us.\n" % 
                             (i + 1, i, (t[i + 1] - t[i]).microseconds))

t = [datetime.now() for i in range(num_marks)]

t[0] = datetime.now()
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

t[1] = datetime.now()
lines=stdin.read().splitlines()
stderr.write("read %d lines.\n" % len(lines))

N, D = map(int, lines[0].split())
stderr.write("N, D = %d, %d\n" % (N, D))

t[2] = datetime.now()
p_list = [0]
count_and_offset = {0:1}

t[3] = datetime.now()
for i in xrange(N):
    price = int(lines[1 + i].rstrip())
    try:
        count_and_offset[price] += 1
    except KeyError:
        count_and_offset[price] = 1
        insort(p_list, price)

t[4] = datetime.now()
cprices = []
cp_sorted = []
for i in xrange(D):
    price = int(lines[1 + N + i])
    insort(cp_sorted, price)
    cprices.append(price)

t[5] = datetime.now()
best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

t[6] = datetime.now()
for day in xrange(D):
    print best_price[cprices[day]]

t[7] = datetime.now()
report_time()
