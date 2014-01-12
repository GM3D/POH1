import bisect
import sys
import itertools


N = 0
D = 0

count = {}
prices = [0]
cprices = []
best_prices = []
tentative_largers = {}

million = int(1e6)
hard_lowest = 10
batch_size = 10000

int_ = int
ord_ = ord
len_ = len
bisect_left = bisect.bisect_left

def find_optimal_price(cp):
    l = []
    lowest_price = prices[1]
    highest_price = prices[-1]
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_left(prices, larger)
    if larger not in count:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if smaller not in count or (count[smaller] == 1 and smaller == larger):
            l.append(larger)
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
    for larger in l:
        smaller = prices[bisect_left(prices, cp - larger) - 1]
        if smaller < lowest_price:
            return 0
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

def find_best_price(cp):
    r = find_optimal_price(cp)
    if r != None:
        return r
    else:
        return find_suboptimal_price(cp)


def myint(s):
    l = len_(s)
    n = i = 0
    while i < l:
        n = n * 10 + ord_(s[i]) - 48
        i += 1
    return n

#@profile
def parse_prices(start, n):
    for i in xrange(start, start + n):
        price = int_(lines[1 + i], 10)
        if price in count:
            count[price] += 1
        else:
            count[price] = 1
            prices.append(price)
    prices.sort()

def parse_cprices():
    global cprices
    cprices = [int_(lines[1 + N + i], 10) for i in xrange(D)]

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
    parse_prices(start, r)
    for day in xrange(D):
        if best_prices[day] != cprices[day]:
            best_prices[day] = find_best_price(cprices[day])

def output():
    output = "\n".join(map(str, best_prices))
    print output

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    N, D = map(int, lines[0].split())
    best_prices = D * [0]
    parse_cprices()
    solve()
    output()
