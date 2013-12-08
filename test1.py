import copy
import random
import subprocess

scripts = (('python', 'challenge6.py'),
           ('python', 'challenge8.py'))

def gen_data(N, D):
    data = "%d %d\n" % (N, D)
    k = random.randrange(5) + 1
    pstep = 10 ** random.randrange(0, k)
    for i in xrange(N):
        price = random.randrange(10, 1000001, pstep)
        data += "%d\n" % price
    for i in xrange(D):
        cprice = random.randrange(10, 1000001)
        data += "%d\n" % cprice
    return data

def compare_outputs(output):
    o1 = output[0].split('\n')
    o2 = output[1].split('\n')
    # print "output[0]:\n", output[0]
    # print "output[1]:\n", output[1]
    for i in xrange(len(o1)):
        try:
            assert o1[i] == o2[i]
        except AssertionError:
            print "i = %s, o1[i] = %s, o2[i] = %s" % (i, o1[i], o2[i])

#countmax = 1
countmax = 10
for count in xrange(countmax):
    print "test run %d of %d" % (count + 1, countmax)
    output = []
    for k in xrange(0, 7): # (0, 7) if fast enough
        N = 10 ** k
        D = random.randrange(1, 76)
        print "N, D = %d, %d" % (N, D)
        data = gen_data(N, D)
        # f = open("data_check.txt", "wt")
        # f.write(data)
        # f.close()
        for i in xrange(2):
            p = subprocess.Popen(scripts[i],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            child_output = p.communicate(data)[0]
            if p.poll() != 0:
                print scripts[i][1] + "didn't end correctly."
                p.terminate()
            output.append(copy.deepcopy(child_output))
        compare_outputs(output)
