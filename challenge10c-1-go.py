# challenge10c-1-go.py ver 0.1
# count_and_offset is list
# with prescan.
# base pure python impl.
# separete count and itable.
# count and itable ctypes and using malloc.

from sys import stdin
from ctypes import CDLL, cast, byref, sizeof, addressof, pointer, POINTER, c_int, c_uint, c_ubyte, c_void_p, c_char_p, c_size_t, c_char

million = 1000 * 1000
max_days = 75
hard_lowest = 10

def ptr_add(ptr, offset):
    address = addressof(ptr.contents) + offset
    return cast(address, POINTER(c_char))

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

libc = CDLL('libc.so.6')

content = stdin.read()
lines=content.splitlines()
N, D = map(int, lines[0].split())

libc.malloc.argtypes = (c_size_t,)
libc.malloc.restype = c_void_p
libc.memset.argtypes = (c_void_p, c_ubyte, c_size_t)
libc.memset.restype = None
libc.strchrnul.argstype = (POINTER(c_char), c_int)
libc.strchrnul.restype = POINTER(c_char)
count = cast(libc.malloc(million + 1), POINTER(c_ubyte))
mark_vp = libc.malloc(million + 2)
mark = cast(mark_vp, POINTER(c_char))
libc.memset(count, 0, million + 1)
libc.memset(mark, ord('.'), million + 1)
mark[million + 1] = '\0'
idxb0_vp = libc.malloc(million + 1)
idxb1_vp = libc.malloc(million + 1)
idxb2_vp = libc.malloc(million + 1)
idxb0 = cast(idxb0_vp, POINTER(c_ubyte))
idxb1 = cast(idxb1_vp, POINTER(c_ubyte))
idxb2 = cast(idxb2_vp, POINTER(c_ubyte))

for i in xrange(N):
    value = int(lines[i + 1])
    count[value] += 1
    mark[value] = 'x'

m = map(int, lines[N + 1:])

ilast = 0
ptr = libc.strchrnul(mark, ord('x'))
ptr_vp = cast(ptr, c_void_p)
i = ptr_vp.value - mark_vp
while i < million + 1:
    idxb0[ilast] = ilast & 0xFF
    idxb1[ilast] = (ilast >> 8) & 0xFF
    idxb2[ilast] = (ilast >> 16) & 0xFF
    libc.memset(idxb0_vp + ilast + 1, idxb0[ilast], i - ilast - 1)
    libc.memset(idxb1_vp + ilast + 1, idxb1[ilast], i - ilast - 1)
    libc.memset(idxb2_vp + ilast + 1, idxb2[ilast], i - ilast - 1)
    ilast = i
    ptr = ptr_add(ptr, 1)
    ptr = libc.strchrnul(ptr, ord('x'))
    ptr_vp = cast(ptr, c_void_p)
    i = ptr_vp.value - mark_vp

idxb0[ilast] = c_ubyte(ilast & 0xFF)
idxb1[ilast] = c_ubyte((ilast >> 8) & 0xFF)
idxb2[ilast] = c_ubyte((ilast >> 16) & 0xFF)
libc.memset(idxb0_vp + ilast + 1, idxb0[ilast], million - ilast)
libc.memset(idxb1_vp + ilast + 1, idxb1[ilast], million - ilast)
libc.memset(idxb2_vp + ilast + 1, idxb2[ilast], million - ilast)

best_price = []
for day in xrange(D):
    best_price.append(find_best_price(m[day]))

for day in xrange(D):
    print best_price[day]
    
    

