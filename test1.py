import copy
import random
import subprocess

scripts = (['./challenge6-c'],
           ['python', 'challenge9f-09.py'])

random.seed()

def gen_data(N, D):
    data = "%d %d\n" % (N, D)
    k = random.randrange(5) + 1
#    pstep = 10 ** random.randrange(0, k)
    pstep = 1
    for i in xrange(N):
        price = random.randrange(10, 1000001, pstep)
        data += "%d\n" % price
    for i in xrange(D):
        cprice = random.randrange(10, 1000001)
        data += "%d\n" % cprice
    return data

def compare_outputs(output, data, k):
    o1 = output[0].split('\n')
    o2 = output[1].split('\n')
    # print "output[0]:\n", output[0]
    # print "output[1]:\n", output[1]
    for i in xrange(len(o1)):
        if not o1[i] == o2[i]:
            print "i = %s, o1[i] = %s, o2[i] = %s" % (i, o1[i], o2[i])
            inputs = data.splitlines()
            N, D = map(int, inputs[0].split())
            price_data = inputs[1:N + 1]
            cprice_data = inputs[N + 1 + i]
            header = "%d %d\n" % (N, 1)
            error_data = header + "\n".join(price_data)
            error_data.join("\n" + cprice_data + "\n")
            print error_data
            f = open("error_data_%d.txt" % k, "wt")
            f.write(error_data)
            f.close()
            return False
    return True
            
#countmax = 1
countmax = 10

def get_name(cmd):
    if cmd[0] in ('python', 'sh', 'bash') and len(cmd) >= 2:
        return cmd[1]
    else:
        if cmd[0].startswith('./'):
            return cmd[0][2:]
        else:
            return cmd[0]

print "comparing %s and %s" % (get_name(scripts[0]), get_name(scripts[1]))

for count in xrange(countmax):
    print "test run %d of %d" % (count + 1, countmax)
    output = []
    for k in xrange(0, 7): # (0, 7) if fast enough
        N = 10 ** k
        D = random.randrange(1, 76)
        print "N, D = %d, %d" % (N, D)
        data = gen_data(N, D)
        f = open("data_check.txt", "wt")
        f.write(data)
        f.close()
        for i in xrange(2):
            p = subprocess.Popen(scripts[i],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            child_output, child_err = p.communicate(data)
            r = p.poll()
            if r != 0:
                print "poll status: " + repr(r)
                print str(scripts[i]) + " didn't end correctly."
                print "Child process error message:" + str(child_err)
                print "Child process output:" + str(child_output)
                p.terminate()
            output.append(copy.deepcopy(child_output))
        if not compare_outputs(output, data, k):
            print "outputs differ on k = %d, N = %d" % (k, N)
            print "test data written into error_data_%d.txt" % k
            exit()
