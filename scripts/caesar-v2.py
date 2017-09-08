#!/bin/env python
# frequency as a fraction of total letters
letterFrequency = [0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007]

input1 = input()

lowerInput = input1.lower()
cipherLetterFrequency = []

# LETTER FREQUENCY CALCULATION:

for letter in range(97,123):
	tempFrequency = 0
	for i in range(len(input1)):
		if ord(lowerInput[i]) == letter:
			tempFrequency += 1
	cipherLetterFrequency.append(tempFrequency / len(lowerInput))

# SHIFT POSSIBILITY CALCULATION:

shiftPossibility = []
for testShift in range(26):
	tempPossibility = 0
	for letter in range(26):
		tempPossibility += cipherLetterFrequency[(letter+testShift)%26] * letterFrequency[letter]
	shiftPossibility.append(tempPossibility)
shiftOrder = [-x for _,x in sorted(zip(shiftPossibility, range(26)))] # returning a list of indexes by possibility
shiftOrder.reverse() # sorted(T) puts the smallest value first - we want the highest

# LETTER SHIFT

for shift in shiftOrder: 
	newInput = ""
	for i in lowerInput:
		if ord(i) < 97 or ord(i) > 122:
			newInput += i
		else:		
			newOrd = (((ord(i)+shift) - 97) % 26 + 97)
			newInput += chr(newOrd)
	print(newInput)
	if input("Is this correct?")[0] == 'y':
		break
