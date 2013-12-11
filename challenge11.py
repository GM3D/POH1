from tempfile import mkstemp
from ctypes import CDLL, c_int, pointer
import os
from base64 import b64decode
binary=""" """
fd, tempfilename = mkstemp(suffix=".so")
f = open(tempfilename, 'wb')
f.write(b64decode(binary))
f.close()
gogo = CDLL(tempfilename)
gogo.zero_readability()
os.remove(tempfilename)
