#!/bin/env python
ab = input("a b ? ").split()
import core,file
ciphertext = file.openAsAscii("cipher.txt")
f = open("output.txt","w")
print(str(core.shiftLinear(lambda x, a, b: a*(x-b), ciphertext, int(ab[0]), int(ab[1])),"utf-8"),file=f)
