# challenge10c.py ver 0.1
# count_and_offset is list
# with prescan.
# base pure python impl.
# separete count and itable.
# count and itable ctypes and using malloc.

import myprofiler
t = myprofiler.ProfileTimer()

t.mark("import")
from sys import stdin
from ctypes import CDLL, cast, byref, sizeof, addressof, POINTER, c_int, c_uint, c_ubyte, c_void_p, c_char_p, c_size_t, c_char

t.mark("defs")
million = 1000 * 1000
max_days = 75
hard_lowest = 10

def get_next_valid_lower(x):
    if count[x]:
        return x
    else:
        i = (int(idxb2[x]) << 16) + (int(idxb1[x]) << 8) + int(idxb0[x])
        return i

def find_best_price(cp):
    candidate = 0
    if cp > 2 * hard_lowest:
        lowlimit = cp / 2
    else:
        lowlimit = hard_lowest
    larger = cp - hard_lowest
    larger = get_next_valid_lower(larger)
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (count[smaller] == 1 and smaller == larger):
            smaller -= 1
        smaller = get_next_valid_lower(smaller)
        if smaller < hard_lowest:
            larger = get_next_valid_lower(larger - 1)
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        larger = get_next_valid_lower(larger - 1)
    return candidate

t.mark("libc initialization")
libc = CDLL('libc.so.6')

t.mark("file read")
content = stdin.read()
lines=content.splitlines()
N, D = map(int, lines[0].split())

t.mark("create itable list")
sizeof_int = 4
libc.malloc.argtypes = (c_size_t,)
libc.malloc.restype = c_void_p
libc.memset.argtypes = (c_void_p, c_ubyte, c_size_t)
libc.memset.restype = None
libc.strchr.argstype = (c_char_p, c_int)
libc.strchr.restype = c_char_p
count = cast(libc.malloc(million + 1), POINTER(c_ubyte))
mark = cast(libc.malloc(million + 1), POINTER(c_char))
libc.memset(count, 0, million + 1)
libc.memset(mark, 0, million + 1)
idxb0_vp = libc.malloc(million + 1)
idxb1_vp = libc.malloc(million + 1)
idxb2_vp = libc.malloc(million + 1)
idxb0 = cast(idxb0_vp, POINTER(c_ubyte))
idxb1 = cast(idxb1_vp, POINTER(c_ubyte))
idxb2 = cast(idxb2_vp, POINTER(c_ubyte))

#idx_vp = libc.malloc((million + 1) * sizeof(c_int))
#idx = cast(idx_vp, POINTER(c_int))

t.mark("count N data")
for i in xrange(N):
    value = int(lines[i + 1])
    count[value] += 1
    mark[value] = 'x'

t.mark("store campaing prices")
m = map(int, lines[N + 1:])

t.mark("prescan index table")

ilast = 0

for i in xrange(million + 1):
    if mark[i] == 'x':
        idxb0[ilast] = ilast & 0xFF
        idxb1[ilast] = (ilast >> 8) & 0xFF
        idxb2[ilast] = (ilast >> 16) & 0xFF
        libc.memset(idxb0_vp + ilast + 1, idxb0[ilast], i - ilast - 1)
        libc.memset(idxb1_vp + ilast + 1, idxb1[ilast], i - ilast - 1)
        libc.memset(idxb2_vp + ilast + 1, idxb2[ilast], i - ilast - 1)
        # for j in xrange(ilast, i):
        #     idx[j] = ilast
        ilast = i
idxb0[ilast] = c_ubyte(ilast & 0xFF)
idxb1[ilast] = c_ubyte((ilast >> 8) & 0xFF)
idxb2[ilast] = c_ubyte((ilast >> 16) & 0xFF)
libc.memset(idxb0_vp + ilast + 1, idxb0[ilast], million - ilast)
libc.memset(idxb1_vp + ilast + 1, idxb1[ilast], million - ilast)
libc.memset(idxb2_vp + ilast + 1, idxb2[ilast], million - ilast)

t.mark("main algorithm")
best_price = []
for day in xrange(D):
    best_price.append(find_best_price(m[day]))

t.mark("print result")
for day in xrange(D):
    print best_price[day]
    
    
t.mark("report")

t.report()
