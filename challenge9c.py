from datetime import datetime, timedelta
t = [datetime.now() for i in range(5)]
import sys

t[0] = datetime.now()
from bisect import bisect_left as bl, insort as ins

lp = 10

def fb(cp):
    ca = 0
    if cp > 2 * lp:
        ll = cp / 2
    else:
        ll = lp
    l = cp - lp
    i = bl(pl, l)
    if not l in m:
        i -= 1
    l = pl[i]
    while l >= ll and ca != cp:
        s = cp - l
        if (not s in m or \
                (m[s] == 1 and cp == 2 * l)):
            s = pl[bl(pl, s) - 1]
        if s < lp:
            i -= 1
            l = pl[i]
            continue
        if s + l > ca:
            ca = s + l
        i -= 1
        l = pl[i]
    return ca

t[1] = datetime.now()
h = raw_input().rstrip().split(' ')
N, D = int(h[0]), int(h[1])
pl = [0]
m = {0:1}
for i in xrange(N):
    p = int(raw_input().rstrip())
    if p in m:
        m[p] += 1
    else:
        m[p] = 1
        ins(pl, p)
cl = []
cs = []
for i in xrange(D):
    p = int(raw_input().rstrip())
    ins(cs, p)
    cl.append(p)

t[2] = datetime.now()
bp = {}
lb = 1
for c in reversed(cs):
    if lb == 0:
        bp[c] = 0
    else:
        bp[c] = lb = fb(c)

t[3] = datetime.now()
for d in xrange(D):
    print bp[cl[d]]

t[4] = datetime.now()
for i in xrange(4):
    sys.stderr.write("t[%d] - t[%d] = %d us.\n" % 
                     (i + 1, i, (t[i + 1] - t[i]).microseconds))
