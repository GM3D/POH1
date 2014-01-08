import myprofiler

t = myprofiler.ProfileTimer()
t.mark("import")
from bisect import bisect_left
import sys

t.mark("defs")
million = int(1e6)
batch_size = 1000

def find_best_price(cp):
    global N, D, lines
    global prices, cprices, count
    global highest_price, lowest_price
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    if larger < lowlimit:
        return 0
    i = bisect_left(prices, larger)
    if not larger in count:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit:
        smaller = cp - larger
        if smaller in count:
            if count[smaller] >= 2:
                return cp
            if count[smaller] == 1 and smaller != larger:
                return cp
        tentative_largers.append(larger)
        i -= 1
        larger = prices[i]
    candidate = 0
    for larger in tentative_largers:
        i = bisect_left(prices, cp -larger) - 1
        smaller = prices[i]
        if smaller + larger > candidate:
            candidate = smaller + larger
    return candidate

def parse_prices(start, n):
    global N, D, lines
    global prices, cprices, count
    global highest_price, lowest_price
    prices = []
    for i in xrange(start, start + n):
        price = int(lines[1 + i])
        if price in count:
            count[price] += 1
        else:
            count[price] = 1
            prices.append(price)
    prices.sort()
    lowest_price = prices[0]
    highest_price = prices[-1]

def solve():
    global best_prices
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
    t.mark("output")
    output = "\n".join(map(str, best_prices))
    print output

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    N, D = map(int, lines[0].split())
    cprices = [int(lines[1 + N + i]) for i in xrange(D)]
    cp_sorted = sorted(cprices)
    cp_min = cp_sorted[0]
    cp_max = cp_sorted[-1]
    count = {0:1}
    prices = []
    best_prices = D * [0]
    solve()
    output()
