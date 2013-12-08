from bisect import bisect_left, bisect

header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
p_list = [0]
multipicity = {0:1}
for i in xrange(N):
    price = int(raw_input().rstrip())
    if price in multipicity:
        multipicity[price] += 1
    else:
        multipicity[price] = 1
        j = bisect(p_list, price)
        p_list.insert(j, price)
cprices = []
for i in xrange(D):
    price = int(raw_input().rstrip())
    cprices.append(price)

best_price = {}
lowest_price = 10
for day in xrange(D):
    candidate = 0
    cp = cprices[day]
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(p_list, larger)
    if not larger in multipicity:
        i -= 1
    larger = p_list[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in multipicity or \
                (multipicity[smaller] == 1 and cp == 2 * larger)):
            smaller = p_list[bisect_left(p_list, smaller) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = p_list[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
        larger = p_list[i]
    best_price[cp] = candidate

for day in xrange(D):
    print best_price[cprices[day]]    
