#!/usr/bin/env python3
import numpy as np
p = input("Possible words in order of certainty: ").split()
inputArray = p
import file, substitution
tupleArray = substitution.tupleArray(file.openAsAscii("cipher.txt"))
print(tupleArray.array[0])
sol = substitution.recursiveSolve(inputArray,tupleArray)
if sol:	
	tupleArray.show()
	print(sol)
else: print("one or more of these words may not exist")