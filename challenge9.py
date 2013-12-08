from bisect import bisect_left, insort

lowest_price = 10

def find_best_price(cp):
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(p_list, larger)
    if not larger in multiplicity:
        i -= 1
        larger = p_list[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in multiplicity or \
                (multiplicity[smaller] == 1 and cp == 2 * larger)):
            smaller = p_list[bisect_left(p_list, smaller) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = p_list[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
        larger = p_list[i]
    return candidate

header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
p_list = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(raw_input().rstrip())
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        insort(p_list, price)
cprices = []
cp_sorted = []
for i in xrange(D):
    price = int(raw_input().rstrip())
    insort(cp_sorted, price)
    cprices.append(price)

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
