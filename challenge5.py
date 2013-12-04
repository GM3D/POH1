import sys
from fractions import gcd

def search_nonzero_downward(start, histgram):
    for i in xrange(start, 0, -1):
        if histgram[i] == 0:
            continue
        else:
            return i

p_hist = 10000001 * [0]
cprices = []
line_num = 0

for line in sys.stdin:
    if line_num == 0:
        header = line.split(' ')
        N, D = int(header[0]), int(header[1])
        p_hist[0] = 1
    elif 0 < line_num and line_num <= N:
        price = int(line)
        p_hist[price] += 1
        if line_num == 1:
            denom = price
        else:
            if denom > 1:
                denom = gcd(denom, price)
    elif N < line_num and line_num <= N + D + 1:
        cprices.append(int(line))
        if denom > 1:
            denom = gcd(denom, int(line))
    line_num += 1

if denom > 1:
    compressed = [p_hist[i] for i in xrange(1000001) if i % denom == 0]
    p_hist = compressed
    cprices2 = [p / denom for p in cprices]
    cprices = cprices2

for day in xrange(D):
    candidate = 0
    cp = cprices[day]
#    minimum = 10 / denom
    larger = cp
    while True:
        larger = search_nonzero_downward(larger - 1, p_hist)
        if larger < cp / 2:
            break
        p_hist[larger] -= 1
        smaller = search_nonzero_downward(cp - larger, p_hist)
        p_hist[larger] += 1
        if not smaller:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    print candidate * denom

