million = 1000000
header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
p_hist = (million + 1) * [0]
for i in xrange(N):
    price = int(raw_input().rstrip())
    p_hist[price] += 1
cprices = []
for i in xrange(D):
    cprices.append(int(raw_input().rstrip()))

next_lower = (million + 1) * [0]

offset = 0
for i in xrange(million + 1):
    next_lower[i] = offset
    if p_hist[i]:
        offset = 0
    offset += 1

best_price = {}
for day in xrange(D):
    candidate = 0
    lowest_price = 10
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
    best_price[cp] = candidate

for day in xrange(D):
    print best_price[cprices[day]]
