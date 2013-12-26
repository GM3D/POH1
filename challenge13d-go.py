#challenge13d.py
# using multiplicity and sorted price list.
# multithreading cprice loop.

import threading
from sys import stdin
lowest_price = 10
threadnum = 16

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

class myThread(threading.Thread):
    def __init__(self, num, id):
        super(myThread, self).__init__()
        self.threadnum = num
        self.id = id
    def run(self):
        i = self.id
        while i < D:
            best_prices[i] = find_best_price(i)
            i += self.threadnum

def find_best_price(day):
    cp = cprices[day]
    candidate = 0
    if cp > 2 * lowest_price:
        lowlimit = cp / 2
    else:
        lowlimit = lowest_price
    larger = cp - lowest_price
    i = bisect_left(prices, larger)
    if not larger in multiplicity:
        i -= 1
        larger = prices[i]
    while larger >= lowlimit and candidate != cp:
        smaller = cp - larger
        if (not smaller in multiplicity or \
                (multiplicity[smaller] == 1 and cp == 2 * larger)):
            smaller = prices[bisect_left(prices, smaller) - 1]
        if smaller < lowest_price:
            i -= 1
            larger = prices[i]
            continue
        if smaller + larger > candidate:
            candidate = smaller + larger
        i -= 1
        larger = prices[i]
    return candidate

lines = stdin.read().splitlines()

N, D = map(int, lines[0].split())
prices = [0]
multiplicity = {0:1}
for i in xrange(N):
    price = int(lines[1 + i])
    if price in multiplicity:
        multiplicity[price] += 1
    else:
        multiplicity[price] = 1
        prices.append(price)

cprices = map(int, lines[1 + N:])
best_prices = [0] * D

prices.sort()

if not threadnum:
    threadnum = D

threads = []
for i in xrange(threadnum):
    threads.append(myThread(threadnum, i))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

for day in xrange(D):
    print best_prices[day]

