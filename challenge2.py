# input_lines = int(raw_input())
# for i in xrange(input_lines):
#   s = raw_input().rstrip().split(',')
#   print "hello = "+s[0]+" , world = "+s[1]

header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
prices = []
for i in xrange(N):
    prices.append(int(raw_input().rstrip()))
#prices.sort()

cprices = []
for i in xrange(D):
    cprices.append(int(raw_input().rstrip()))

for day in xrange(D):
    candidate = 0
    smaller_prices = [p for p in prices if p <= cprices[day] / 2]
    larger_prices = [p for p in prices if p >= cprices[day] / 2]
    for smaller in smaller_prices:
        for larger in larger_prices:
            if smaller + larger <= cprices[day] and smaller + larger > candidate:
                candidate = smaller + larger
    print candidate

    
