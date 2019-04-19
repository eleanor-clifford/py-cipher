try: import file
except ImportError: from src import file
from math import sqrt

a = file.openAsAscii("/home/el/Projects/py-cipher/cipher.txt")

a = str(a,"ascii")
a = a.replace("\n","").replace(" ","")
l = len(a)
factors = [l]
for i in range(2,int(sqrt(l)) + 1):
	if l%i == 0: factors.append(i)

print(sorted(factors))