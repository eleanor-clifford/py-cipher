#!/usr/bin/env python3
''' 
Uses the core and dictionary modules to test for Affine ciphers (includes Caesar and Atbash)

Sample Usage
$ ./test-all.py
ZGGZX PZGWZ DM
AFFINE TEST...SUCCESS
attack at dawn
D(x): x -> 25(x-11) mod 26
'''
import core, dictionary
COPRIMES = [1,3,5,7,9,11,15,17,19,21,23,25] # coprimes of 26 - the modular multiplicative inverse is the same set
input1 = input()
f = core.frequencyList(input1)
print("AFFINE TEST...",end="")
affineShiftList = core.sortLinear(lambda x, a, b: a*(x - b), input1, COPRIMES, range(26), f)
affine = dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b),input1,affineShiftList)
if affine: 
    print("SUCCESS")
    print(affine[0])
    print("D(x): x -> ",affine[1][0],"(x","-",affine[1][1],") mod 26",sep="")
else: 
    print("FAILED")
