#!/usr/bin/env python3
import core, dictionary
input1 = input()
f = core.frequencyList(input1)
print("AFFINE TEST...",end="")
affineShiftList = core.sortLinear(lambda x, a, b: a*x + b, input1, range(1,12), range(26), f)
affine = dictionary.filterIgnoreSpace(lambda x, a, b: a*x + b,input1.replace(" ",""),affineShiftList)
if affine: 
    print("SUCCESS")
    print(affine[0])
    print("x -> ",affine[1][0],"x","+",affine[1][1],sep="")
else:
    print("FAILED")
    print("ATBASH TEST...",end="")
    atbashShiftList = core.sortLinear(lambda x, a, b: -(a*x) + b, input1, range(1,12), range(26), f)
    atbash = dictionary.filterIgnoreSpace(lambda x, a, b: -(a*x) + b,input1.replace(" ",""),atbashShiftList)
    if atbash: 
        print("SUCCESS")
        print(atbash[0])
        print("x -> -",atbash[1][0],"x","+",atbash[1][1],sep="")
    else: print("FAILED")
