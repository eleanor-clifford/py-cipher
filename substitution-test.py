#!/usr/bin/env python3
import numpy as np
p = input("Possible words in order of certainty: ").split()
inputArray = np.zeros(len(p),dtype="object")
for i,word in enumerate(p):
	inputArray[i] = bytearray(word,"ascii")
import file, substitution
tupleArray = substitution.tupleArray(file.openAsAscii("cipher.txt"))
a = substitution.cipherAlphabet()
accepted = []
for word in inputArray:
	for ciphertext in substitution.wordPossibilities(word,tupleArray):
		a.set(word,ciphertext)
		substitution.shift(a,tupleArray)
		if substitution.partialCheck(tupleArray): 
			print(word,ciphertext)
			accepted.append((word,ciphertext))
			break
		else:
			tupleArray.scrap()
			a.scrap()
			for i,j in accepted: a.set(i,j)
	else: 
		print("NO SOLUTIONS")
		raise SystemExit
print(tupleArray.show())