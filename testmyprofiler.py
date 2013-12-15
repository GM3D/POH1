import myprofiler

t = myprofiler.ProfileTimer()
million = 1000000

t.mark("list creation with zero fill")
l = [0] * million
t.mark("end")

t.report()
