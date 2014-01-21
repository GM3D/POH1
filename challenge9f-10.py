import bisect
import sys
import itertools

batch_size = 15000

N = 0
D = 0
prices = [0]
total_prices = [0]
cprices = []
best_prices = []
tentative_largers = {}
lines = []

int_ = int
len_ = len
bisect_left = bisect.bisect_left
bisect_right = bisect.bisect_right
imap = itertools.imap
islice = itertools.islice
split = str.split
append = list.append

def find_optimal_price(cp):
    l = []
    lowest_price = prices[1]
    highest_price = prices[-1]
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_right(prices, larger) - 1
    larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        j = bisect_left(prices, smaller)
        if prices[j] != smaller or (prices[j] == smaller and smaller == larger):
            append(l, larger)
            i -= 1
            larger = prices[i]
            continue
        else:
            return cp
    tentative_largers[cp] = l
    return None

def find_suboptimal_price(cp):
    lowest_price = prices[1]
    highest_price = prices[-1]
    l = tentative_largers[cp]
    candidate = 0
    last_larger = 0
    for larger in l:
        if larger != last_larger:
            smaller = prices[bisect_left(prices, cp - larger) - 1]
            if smaller < lowest_price:
                return 0
            if smaller + larger > candidate:
                candidate = smaller + larger
        last_larger = larger
    return candidate

def find_best_price(cp):
    r = find_optimal_price(cp)
    if r != None:
        return r
    else:
        return find_suboptimal_price(cp)

def parse_prices(start, n):
    global prices
    l = imap(myint, islice(lines, 1 + start, 1 + start + n))
    prices += l
    prices.sort()

def parse_cprices():
    global cprices
    cprices = tuple(imap(myint, islice(lines, 1 + N, 1 + N + D)))

def solve():
    start = 0
    count = D
    d, r = divmod(N, batch_size)
    for i in xrange(d):
        parse_prices(start, batch_size)
        for day in xrange(D):
            if best_prices[day] != cprices[day]:
                x = find_best_price(cprices[day])
                best_prices[day] = x
                if x == cprices[day]:
                    count -= 1
        if count == 0:
            return
        start += batch_size
    if r:
        parse_prices(start, r)
    for day in xrange(D):
        if best_prices[day] != cprices[day]:
            best_prices[day] = find_best_price(cprices[day])


def output():
    output = "\n".join(map(str, best_prices))
    print output


def myint(s):
    return int_(s, 10)

lines = split(sys.stdin.read().rstrip(), '\n')
N, D = imap(myint, split(lines[0]))
best_prices = D * [0]
parse_cprices()
solve()
output()