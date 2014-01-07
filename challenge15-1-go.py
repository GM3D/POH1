import sys
from bisect import bisect_left, bisect_right

class Campaign:
    def __init__(self):
        self.best_prices = {}

    def input(self, f):
        self.lines = f.read().splitlines()
        self.N, self.D = map(int, self.lines[0].split())
        self.p = [int(self.lines[1 + i]) for i in xrange(self.N)]
        self.p.sort()
        self.cprices = [int(self.lines[1 + self.N + i]) for i in xrange(self.D)]
        self.cp_sorted = sorted(self.cprices)

    def solve(self):
        for cp in self.cp_sorted:
            c = self.find_best_price(cp)
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

    def output(self, f):
        result = [str(self.best_prices[self.cprices[day]]) 
                  for day in xrange(self.D)]
        f.write("\n".join(result) + "\n")

if __name__ == '__main__':
    c1 = Campaign()
    c1.input(sys.stdin)
    c1.solve()
    c1.output(sys.stdout)
