from bisect import bisect_left, bisect_right
import sys
import itertools

million = int(1e6)
batch_size = 20000
int_=int

def find_best_price(cp):
    global N, D, lines
    global prices, cprices
    global highest_price, lowest_price
    tentative_largers = []
    lowlimit = max(cp / 2, lowest_price)
    larger = min(cp - lowest_price, highest_price)
    candidate = 0
    if larger < lowlimit:
        return 0
    i = bisect_right(prices, larger) - 1
    while larger >= lowlimit:
        larger = prices[i]
        smaller = cp - larger
        j = bisect_left(prices, smaller)
        if j > i:
            i -= 1
            continue
        if prices[j] != smaller or i == j:
            j -= 1
        smaller = prices[j]
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
    return candidate

def parse_prices(start, n):
    global N, D, lines
    global prices, cprices, count
    global highest_price, lowest_price
    prices.extend(list(itertools.imap(int_, (lines[1 + i] for i in xrange(start, n)))))
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
