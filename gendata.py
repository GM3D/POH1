import random

def gen_data(N, D):
    data = "%d %d\n" % (N, D)
    k = random.randrange(5) + 1
    pstep = 10 ** random.randrange(0, k)
    for i in xrange(N):
#        price = random.randrange(10, 1000001, pstep)
        price = random.randrange(10, 1000001)
        data += "%d\n" % price
    for i in xrange(D):
        cprice = random.randrange(10, 1000001)
        data += "%d\n" % cprice
    return data

print gen_data(500000, 75)
