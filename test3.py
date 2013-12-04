try:
    while True:
        line = raw_input()
        print "subprocess;"+line
except EOFError:
    pass
