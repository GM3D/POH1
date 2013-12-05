def search_nonzero_downward(start, histgram):
    for i in xrange(start, 9, -1):
        if histgram[i]:
            return i
    return -1


header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
p_hist = 1000001 * [0]
for i in xrange(N):
    price = int(raw_input().rstrip())
    p_hist[price] += 1
cprices = []
for i in xrange(D):
    cprices.append(int(raw_input().rstrip()))

for day in xrange(D):
    candidate = 0
    cp = cprices[day]
    larger = cp - 10
    while True:
        larger = search_nonzero_downward(larger - 1, p_hist)
        if larger < cp / 2 or larger < 10:
            break
        p_hist[larger] -= 1
        smaller = search_nonzero_downward(cp - larger, p_hist)
        p_hist[larger] += 1
        if smaller < 10:
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
    print candidate

