import subprocess

cmd = ('python', './test3.py')

p = subprocess.Popen(cmd, 
                     stdin=subprocess.PIPE, 
                     stdout=subprocess.PIPE)

lineno = 0
while lineno < 3:
    line = raw_input()
    print "parent; " + line
    child_output = p.communicate(line)[0]
    print child_output
p.terminate()

