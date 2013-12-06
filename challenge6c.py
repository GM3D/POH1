from datetime import datetime, timedelta
t = [datetime.now() for i in range(9)]
import sys


t[0] = datetime.now()
#from fractions import gcd
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

million = 1000000

t[1] = datetime.now()
header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])

t[2] = datetime.now()
p_hist = (million + 1) * [0]

t[3] = datetime.now()
for i in xrange(N):
    price = int(raw_input().rstrip())
    p_hist[price] += 1
    if i == 0:
        denom = price
    else:
        if denom > 1:
            denom = gcd(denom, price)

cprices = []
for i in xrange(D):
    price = int(raw_input().rstrip())
    cprices.append(price)
    if denom > 1:
        denom = gcd(denom, price)

t[4] = datetime.now()
if denom > 1:
    p_hist = [p_hist[i * denom] for i in xrange(million / denom + 1)]
    cprices = [p / denom for p in cprices]
    million /= denom

t[5] = datetime.now()
next_lower = (million + 1) * [0]

t[6] = datetime.now()
offset = 0
for i in xrange(million + 1):
    next_lower[i] = offset
    if p_hist[i]:
        offset = 0
    offset += 1

t[7] = datetime.now()
for day in xrange(D):
    candidate = 0
    lowest_price = 10 / denom
    cp = cprices[day]
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    if not p_hist[larger]:
        larger -= next_lower[larger]
    while larger >= lowlimit:
        smaller = cp - larger
        if (not p_hist[smaller]) or \
        (p_hist[smaller] == 1 and cp == 2 * larger):
            smaller -= next_lower[smaller]
        if smaller < lowest_price:
            larger -= next_lower[larger]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        larger -= next_lower[larger]
    print candidate * denom

t[8] = datetime.now()

for i in range(8):
    sys.stderr.write("t[%d] - t[%d] = %d us.\n" % 
                     (i + 1, i, (t[i + 1] - t[i]).microseconds))
