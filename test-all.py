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
import core, dictionary, key
from TWL06 import twl
COPRIMES = [1,3,5,7,9,11,15,17,19,21,23,25] # coprimes of 26 - the modular multiplicative inverse is the same set
cipher = input()
f = core.frequencyList(cipher)
print("AFFINE TEST...",end="")
affineShiftList = core.sortLinear(lambda x, a, b: a*(x - b), cipher, COPRIMES, range(26), f)
affine = dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b),cipher,affineShiftList)
if affine: 
    print("SUCCESS")
    print(affine[0])
    print("D(x): x -> ",affine[1][0],"(x","-",affine[1][1],") mod 26",sep="")
else: 
    print("FAILED")
    print("KEYWORD TEST...",end="")
    words = set(twl.iterator())
    for word in words:
        cipherAlphabet = key.fixDouble(word + "abcdefghijklmnopqrstuvwxyz")
        decrypted = key.shift(cipher,cipherAlphabet)
        keyword = dictionary.recursiveCheck(decrypted.replace(" ",""))
        if keyword[0]:
            print("SUCCESS")
            print("is",keyword[1],"english? ",end="")
            if input()[0] == 'y':
                print("Keyword is",word)
                break
            else:
                print("KEYWORD TEST...",end="")
    else:
        print("FAILED")
        print("RANDOM KEY TEST...")
        MAX_LENGTH = 10
        for length in range(1,MAX_LENGTH):
            if length > 1: 
                print("FAILED")
            print("\t",length,"LETTER WORDS...",end="")
            for x in range(26**length):
                output = ""
                while x > 0:
                    output += chr(97+x%26)
                    x = x//26
                cipherAlphabet = key.fixDouble(output[::-1] + "abcdefghijklmnopqrstuvwxyz")
                decrypted = key.shift(cipher,cipherAlphabet)
                keyword = dictionary.recursiveCheck(decrypted.replace(" ",""))
                if keyword[0]:
                    print("SUCCESS")
                    print("is",keyword[1],"english? ",end="")
                    if input()[0] == 'y':
                        print("Keyword is",word)
                        break
                    else:
                        print("RANDOM KEY TEST...",end="")
        


