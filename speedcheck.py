import sys

from datetime import datetime, timedelta
from sys import stderr

num_marks = 10
def report_time():
    for i in xrange(num_marks - 1):
        if t[i+1] > t[i]:
            stderr.write("t[%d] - t[%d] = %d us.\n" % 
                             (i + 1, i, (t[i + 1] - t[i]).microseconds))

t = [datetime.now() for i in range(num_marks)]


def regular_read():
    return  sys.stdin.read()

def read_and_parse():
    t[0] = datetime.now()
    content = regular_read()
    t[1] = datetime.now()
    lines = content.split('\n')
    print "%d lines." % len(lines)
    t[2] = datetime.now()


read_and_parse()
report_time()

