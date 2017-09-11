'''
Common Functions for cipher cracking
'''
import twl

def frequencyList(input1):
	cipherLetterFrequency = []
	for letter in range(97,123):
		tempFrequency = 0
		for i in input1:
			if ord(i.lower()) == letter:
				tempFrequency += 1
		cipherLetterFrequency.append(tempFrequency) # / len(input1))
	return cipherLetterFrequency

def sort(function, list1, parameters, cipherLetterFrequency):
	'''
	sorts list1 by function(letter,param) with respect to a cipherLetterFrequency
	
	Caesar cipher example:
	>>> sort(lambda a, b: a + b, range(26), range(26), core.frequencyList(input()))
	'''
	letterFrequency = [0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007] 
	shiftPossibility = []
	for param in parameters:
		tempPossibility = 0
		for letter in range(26):
			tempPossibility += cipherLetterFrequency[(function(letter,param))%26] * letterFrequency[letter]
		shiftPossibility.append(tempPossibility)
	return [-x for _,x in sorted(zip(shiftPossibility, range(26)))][::-1]
	

def sortLinear(function, list1, a, b, cipherLetterFrequency):
	letterFrequency = [0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007] 
	shiftPossibility = []
	paramList = []
	for param1 in a:
		for param2 in b:
			tempPossibility = 0
			for letter in range(26):
				tempPossibility += cipherLetterFrequency[(function(letter,param1,param2))%26] * letterFrequency[letter]
			shiftPossibility.append(tempPossibility)
			paramList.append((param1,param2))
	print(len(shiftPossibility))
	return [(a,-b) for _,(a,b) in sorted(zip(shiftPossibility, paramList))][::-1]

def caesarShiftNoCheck(function,list1,param):
	newInput = ""
	for i in list1.lower():
		if ord(i) < 97 or ord(i) > 122:
			newInput += i
		else:		
			newInput += chr((function(ord(i),param) - 97) % 26 + 97)
	return newInput
def shift(function, list1, parameters):
	'''
	shifts list1 by function(letter,param) with respect to a cipherLetterFrequency
	
	Caesar cipher example:
	>>> shift(lambda a, b: a + b, list1, sortedShiftList)
	'''
	for param in parameters: 
		newInput = ""
		for i in list1.lower():
			if ord(i) < 97 or ord(i) > 122:
				newInput += i
			else:		
				newInput += chr((function(ord(i),param) - 97) % 26 + 97)
		print(newInput)
		if input("Is this correct? ")[0] == "y":
			break

def shiftLinearNoCheck(function, list1, a, b):
	newInput = ""
	for i in list1.lower():
		if ord(i) < 97 or ord(i) > 122:
			newInput += i
		else:		
			newInput += chr((function(ord(i),a,b) - 97) % 26 + 97)
	return newInput

