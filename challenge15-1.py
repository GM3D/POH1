import myprofiler
t = myprofiler.ProfileTimer()

t.mark("import")
import sys
from bisect import bisect_left, bisect_right

t.mark("defs")
class Campain:
    def __init__(self):
        self.best_prices = {}

    def input(self, f):
        self.lines = f.read().splitlines()
        self.N, self.D = map(int, self.lines[0].split())
        self.p = [int(self.lines[1 + i]) for i in xrange(self.N)]
        self.p.sort()
        self.pp = []
        d, r = divmod(len(self.p), 3)
        for i in xrange(d):
            p = self.p
            self.pp += (p[i] + p[i + 1], p[i] + p[i + 2], p[i + 1] + p[i + 2])
        if r == 2:
            self.pp.append(p[-1] + p[-2])
        self.cprices = [int(self.lines[1 + self.N + i]) for i in xrange(self.D)]
        self.cp_sorted = sorted(self.cprices)
        # print "N, D = %d, %d" % (self.N, self.D)
        # print "prices =", self.p
        # print "cprices =", self.cprices
        # print "cp_sorted =", self.cp_sorted

    def solve(self):
        for cp in self.cp_sorted:
#            print "cp = ", cp
            c = self.find_best_price_wrapper(cp)
            self.best_prices[cp] = c

    def find_best_price(self, cp):
        p = self.p
        candidate = 0
        i = 0
        j = len(p) - 1
        while i != j:
            s = p[i] + p[j]
            if s == cp:
                return cp
            elif s > cp:
                j -= 1
            else:
                i += 1
                if candidate < s:
                    candidate = s
        return candidate

    def find_best_price_wrapper(self, cp):
        return self.find_best_price(cp)

    def output(self):
        for day in xrange(self.D):
            print self.best_prices[self.cprices[day]]

t.mark("main")
if __name__ == '__main__':
    t.mark("instance creation")
    c1 = Campain()
    t.mark("data read")
    c1.input(sys.stdin)
    t.mark("solve")
    c1.solve()
    t.mark("output")
    c1.output()
    t.mark("report")
    t.report()
