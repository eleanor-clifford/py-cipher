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
		tupleArray.scrap()
		a.scrap()
		a.set(word,ciphertext)
		for i,j in accepted: a.set(i,j)
		print(a.current[0])
		substitution.shift(a,tupleArray)
		#print(tupleArray.array[0])
		if substitution.partialCheck(tupleArray): 
			print(word,ciphertext)
			accepted.append((word,ciphertext))
			print(tupleArray.array[0])
			break
	else: 
		print("NO SOLUTIONS")
		raise SystemExit
print(tupleArray.array[0])
print(tupleArray.show())