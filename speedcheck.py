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

def stdin_readlines():
    lines=sys.stdin.readlines()

def regular_read():
    return  sys.stdin.read()

def parsegenerator(s, n)
    while(count < 0):
        if s(i) == '\n':
            count += 1
            yield value
        else:
            value = value * 10 + ord(s[i]) - ord('0')
        i += 1

parsegenerator.i = 0
parsegenerator.count = 0
parsegenerator.value = 0
        
def generator_and_counter():
    content = regular_read()
    i = find(content, ' ')
    N = int(content[:i])
    j = find(content, '\n')
    D = int(content[i + 1:j])
    src = parsegenerator(content[j+1:], N)
    count = Counter((p for p in src))
    cprices = [p for p in src
                    
                     
    

def read_and_parse():
    t[0] = datetime.now()
#    content = regular_read()
    t[1] = datetime.now()
#    lines = content.splitlines()
    lines=sys.stdin.readlines()
    print "%d lines." % len(lines)
    t[2] = datetime.now()


read_and_parse()
report_time()

