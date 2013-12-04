import cProfile
import random

def search_binary(value, array):
    """find i such that array[i - 1] <= value and value < array[i].
    array must be sorted."""
    l = len(array)
    i = step = l / 2
    while True:
        if i  < l and array[i] <= value:
            i += step
        elif i >= 1 and value < array[i - 1]:
            i -= step
        else:
            break
        step /= 2
        if step == 0:
            step = 1
    return i

def solve(N=0, D=0, prices=None, cprices=None):
    if N == 0 and D == 0:
        header = raw_input().rstrip().split(' ')
        N, D = int(header[0]), int(header[1])
    if not prices:
        prices = []
        for i in xrange(N):
            prices.append(int(raw_input().rstrip()))
        prices.sort()
    if not cprices:
        cprices = []
        for i in xrange(D):
            cprices.append(int(raw_input().rstrip()))
    for day in xrange(D):
        candidate = 0
        cp = cprices[day]
        index0 = search_binary(cp, prices)
        for i in xrange(index0):
            smaller = prices[i]
            j = search_binary(cp - smaller, prices) - 1
            if j == i:
                j -= 1
            if j < 0:
                continue
            larger = prices[j]
            if smaller + larger > candidate:
                candidate = smaller + larger
        print candidate

if __name__ == '__main__':
    N, D = 1000000, 75
    prices = map(lambda x: x * random.randrange(10, 1000001), N*[1])
    cprices = map(lambda x: x * random.randrange(10, 1000001), D*[1])
    cProfile.run("solve(N, D, prices, cprices)")
