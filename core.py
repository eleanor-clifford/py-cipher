'''
A few common functions for cipher cracking

Functionality:

- Return a list of letter frequency from a given string
- Sort a string with a given linear function into a list of inputs based on letter frequency
- Shift a given string based on a linear function and inputs

Sample Usage:
>>> from cipher import core
>>> letterFrequency = core.frequencyList(<encrypted bytearray>)
>>> core.sortLinear(lambda x, a, b: a*x + b,<encrypted bytearray>,range(1,5),range(26))
[(<a1>,<b1>),(<a2>,<b2>)...(<a104>,<b104>)]
>>> core.shiftLinear(lambda x, a, b: a*x + b,<encrypted bytearray>,<a1>,<b1>)
<decrypted string>
'''

def frequencyList(input1,utf8=False):
	'''
	Returns a list of the frequency of characters in a string as fractions of the total

	>>> frequencyList("abcde",utf8=True)
	[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	>>> frequencyList(bytearray("abcde","ascii"))
	[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	'''
	cipherLetterFrequency = []
	for letter in range(97,123):
		tempFrequency = 0
		for i in input1.lower():
			if utf8:
				if ord(i) == letter: tempFrequency += 1
			elif i == letter:
				tempFrequency += 1
		cipherLetterFrequency.append((tempFrequency))
	return cipherLetterFrequency

def sortLinear(function, list1, a, b, cipherLetterFrequency):
	'''
	Returns a list of possible values for a given function 
	sorted by similarity of the letter frequency to english

	>>> core.sortLinear(lambda x, a, b: a*x + b,<encrypted string>,range(1,5),range(26))
	[(<a1>,<b1>),(<a2>,<b2>)...(<a104>,<b104>)]
	'''
	letterFrequency = [0.0817, 0.0149, 0.0278, 0.0425, 0.127, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007] 
	shiftPossibility = []
	paramList = []
	for param1 in a:
		for param2 in b:
			tempPossibility = 0
			for letter in list1:
				if 65 <= letter <= 90:
					newLetter = (function(letter-65,param1,param2))%26
					tempPossibility += letterFrequency[newLetter]
			shiftPossibility.append(tempPossibility)
			paramList.append((param1,param2))
	return [(a,b) for _,(a,b) in sorted(zip(shiftPossibility, paramList))][::-1]

def shiftLinear(function, list1, a, b, utf8=False):
	'''
	Shifts a given string by the function and two input values `a` and `b`
	>>> core.shiftLinear(lambda x, a, b: a*(x - b),"NGGNPX NG QNJA",1,13,utf8=True)
	'attack at dawn'
	>>> core.shiftLinear(lambda x, a, b: a*(x - b),bytearray("NGGNPX NG QNJA","ascii"),1,13)
	bytearray(b'attack at dawn')
	'''
	if utf8:
		newInput=""
		for i in list1.lower():
			if ord(i) < 97 or ord(i) > 122:
				newInput += i
			else:		
				newInput += chr((function(ord(i)-97,a,b) % 26 + 97))
		return newInput
	else:
		newInput = bytearray("","ascii")
		for i in list1.lower():
			if i < 97 or i > 122:
				newInput += bytes([i])
			else:		
				newInput += bytes([(function(i-97,a,b)) % 26 + 97])
		return newInput

