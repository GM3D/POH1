# input_lines = int(raw_input())
# for i in xrange(input_lines):
#   s = raw_input().rstrip().split(',')
#   print "hello = "+s[0]+" , world = "+s[1]

header = raw_input().rstrip().split(' ')
N, D = int(header[0]), int(header[1])
prices = []
for i in xrange(N):
    prices.append(int(raw_input().rstrip()))
cprices = []
for i in xrange(D):
    cprices.append(int(raw_input().rstrip()))

for day in xrange(D):
    candidate = 0
    for i in xrange(N):
        smaller = prices[i]
        if(smaller > cprices[day] / 2):
            continue
        for j in xrange(N):
            larger = prices[j]
            sum = smaller + larger
            if larger < smaller or j == i:
                continue
            if sum > candidate and sum <= cprices[day]:
                candidate = sum
    print candidate

    
