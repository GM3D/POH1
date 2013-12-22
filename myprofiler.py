from datetime import datetime
from sys import stderr

class ProfileTimer:
      def __init__(self):
            self.timers = []
            self.descriptions = []
      def mark(self, description):
            self.timers.append(datetime.now())
            self.descriptions.append(description)
      def report(self):
            for i in xrange(len(self.timers) - 1):
                  if self.timers[i+1] > self.timers[i]:
                        stderr.write("%s (t[%d] - t[%d]) = %d us.\n" % 
                                     (self.descriptions[i], i + 1, i, 
                                      (self.timers[i + 1] - self.timers[i]).
                                      microseconds))
