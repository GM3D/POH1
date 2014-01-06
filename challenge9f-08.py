import myprofiler

t = myprofiler.ProfileTimer()
t.mark("import")
from bisect import bisect_left
import sys

t.mark("defs")
million = int(1e6)
max_days = 50

@profile
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
        else:
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

@profile
def read_input():
    global N, D, lines
    lines = sys.stdin.read().splitlines()
    N, D = map(int, lines[0].split())

def parse_cprices():
    global N, D, lines
    global prices, cprices, count
    cprices = [int(lines[1 + N + i]) for i in xrange(D)]
    cp_sorted = sorted(cprices)
    cp_min = cp_sorted[0]
    cp_max = cp_sorted[-1]

@profile
def parse_prices():
    global N, D, lines
    global prices, cprices, count
    global highest_price, lowest_price
    count = {0:1}
    prices = []
    for i in xrange(N):
        price = int(lines[1 + i])
        if price in count:
            count[price] += 1
        else:
            count[price] = 1
            prices.append(price)
    prices.sort()
    lowest_price = prices[0]
    highest_price = prices[-1]

@profile
def main():
    global N, D, lines
    global prices, cprices, count
    best_prices = [find_best_price(cprices[day]) for day in xrange(D)]
    t.mark("output")
    output = "\n".join(map(str, best_prices))
    print output

if __name__ == '__main__':
    t.mark("read data")
    read_input()
    t.mark("fill cprices")
    parse_cprices()
    t.mark("fill prices count")
    parse_prices()
    t.mark("main algorithm")
    main()
    t.mark("report")
    t.report()
