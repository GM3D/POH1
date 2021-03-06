#challenge10c.py
# count_and_offset is list
# with prescan.

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
from sys import stdin

def get_next_valid_lower(x):
    l = count_and_offset[x]
    if l < 0:
        x += l
    return x

million = 1000 * 1000
max_days = 75
lowest_price = 10

t[1] = datetime.now()
content = stdin.read()
lines=content.splitlines()

N, D = map(int, lines[0].split())

t[2] = datetime.now()
count_and_offset = [0] * (million + 1)
t[3] = datetime.now()
for i in xrange(N):
    value = int(lines[i + 1])
    count_and_offset[value] += 1

cprices = map(int, lines[N + 1:])

t[4] = datetime.now()
offset = 0;
for i in xrange(million + 1):
    if count_and_offset[i] > 0:
            offset = 0;
    else:
        count_and_offset[i] = offset
    offset -= 1

t[5] = datetime.now()
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

t[6] = datetime.now()
for day in xrange(D):
    print best_price[day]
    
t[7] = datetime.now()

report_time()
