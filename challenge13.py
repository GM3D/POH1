#challenge13.py
# using multiplicity and sorted price list.
# with self-made bisect and raw input.

lowest_price = 10

def bisect_left(array, value):
    l = len(array)
    i = step = l / 2
    while True:
        if i  < l and array[i] < value:
            i += step
        elif i >= 1 and value <= array[i - 1]:
            i -= step
        else:
            break
        step /= 2
        if step == 0:
            step = 1
    return i

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

N, D = map(int, raw_input().rstrip().split())
p_list = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(input())
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        p_list.append(price)

cprices = []
for i in xrange(D):
    cprices.append(int(input()))

p_list.sort()
cp_sorted = sorted(cprices)

best_price = {}
last_best = 1
for c in reversed(cp_sorted):
    if last_best == 0:
        best_price[c] = 0
    else:
        best_price[c] = last_best = find_best_price(c)

for day in xrange(D):
    print best_price[cprices[day]]
