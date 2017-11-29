import ctypes, numpy as np, os

_hill = ctypes.CDLL(os.path.realpath(os.path.dirname(__file__))+'/libhill.so')
_hill.frequencyAnalysis.argtypes = (ctypes.c_char_p,ctypes.c_int)
_hill.frequencyAnalysis.restype = ctypes.POINTER(ctypes.c_float)

def frequencyAnalysis(N, ciphertext):
	global _hill
	ciphertext=bytes(ciphertext)
	out = ctypes.POINTER(ctypes.c_float * (26 ** N))()
	_hill.frequencyAnalysis(ctypes.c_char_p(ciphertext),ctypes.c_int(N),ctypes.byref(out))
	return np.array(out.contents)