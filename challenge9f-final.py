import bisect
import sys
import itertools

sys.setcheckinterval(100000)

batch_size = 15000

N = 0
D = 0
prices = None
cprices = []
best_prices = []
tentative_largers = {}

int_ = int
len_ = len
bisect_left = bisect.bisect_left
bisect_right = bisect.bisect_right
imap = itertools.imap
islice = itertools.islice
repeat = itertools.repeat
split = str.split
append = list.append
extend = list.extend
sort = list.sort

def find_optimal_price(cp):
    l = []
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

def parse_prices(body, n):
    global prices, lowest_price, highest_price
    lines = split(body, '\n', n)
    l = imap(int_, lines[:-1], repeat(10))
    if not prices:
       prices = list(l)
       prices.append(0)
    else:
       extend(prices, l)
    prices.sort()

    lowest_price = prices[1]
    highest_price = prices[-1]
    return lines[-1]

def parse_cprices():
    global cprices
    lines = content.rsplit('\n', D)
    cprices = tuple(imap(int_, lines[1:]))

def solve():
    global body
    count = D
    d, r = divmod(N, batch_size)
    for i in xrange(d):
        body = parse_prices(body, batch_size)
        for day in xrange(D):
            if best_prices[day] != cprices[day]:
                x = find_best_price(cprices[day])
                best_prices[day] = x
                if x == cprices[day]:
                    count -= 1
        if count == 0:
            return
    if r:
        parse_prices(body, r)
        for day in xrange(D):
            if best_prices[day] != cprices[day]:
                best_prices[day] = find_best_price(cprices[day])


def output():
    output = "\n".join(map(str, best_prices))
    print output

content = sys.stdin.read().rstrip()
s_content = split(content, '\n', 1)
N, D = imap(int_, s_content[0].split())
body = s_content[-1]
best_prices = D * [0]
parse_cprices()
solve()
output()
