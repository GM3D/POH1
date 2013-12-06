import tempfile
from ctypes import CDLL, c_int, pointer

header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
p_hist = 1000001 * [0]
for i in xrange(N):
    price = int(raw_input().rstrip())
    p_hist[price] += 1
cprices = []
for i in xrange(D):
    cprices.append(int(raw_input().rstrip()))

tempfile.mkstemp(suffix=".so")
lib = CDLL("libc.so.6")

for day in xrange(D):
    candidate = 0
    cp = cprices[day]
    larger = cp - 10
    while True:
        found = False
        for i in xrange(larger - 1, 9, -1):
            if p_hist[i]:
                larger = i
                found = True
                break
        if not found:
            larger = -1
        if larger < cp / 2 or larger < 10:
            break
        p_hist[larger] -= 1
        found = False
        for i in xrange(cp - larger, 9, -1):
            if p_hist[i]:
                smaller = i
                found = True
                break
        if not found:
            smaller = -1
        p_hist[larger] += 1
        if smaller < 10:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    print candidate

