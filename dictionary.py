'''
A few common functions for checking possible solutions

Functionality:
- Recursively check against a scrabble dictionary and list of one letter words and return a Boolean and the decrypted cipher

Sample Usage:

>>> from cipher import dictionary
>>> dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b), <affine cipher>, <list of possible shifts as (a,b)>)
<decrypted cipher>

Depends: cipher.core.shiftLinear, twl
'''
from TWL06 import twl
from core import shiftLinear

def filter(function,cipher,sortedShiftList): # last is tuple 
	'''
	Checks each word of an input, shifted by the function and looping through a list of inputs, `sortedShiftList` 
	against the scrabble dictionary and returns a decrypted string if it passes
	Returns None if none of the possibilities pass the test

	>>> filter(lambda x, a, b: a*(x - b), "NGGNPX NG QNJA", [(5,1),(3,4),(1,13)])
	'attack at dawn'
	''' 

	FAILURE_THRESHOLD = 0.2
	for param in sortedShiftList:
		input1 = shiftLinear(function,cipher,param[0],param[1])
		inputList = input1.split()
		failRate = FAILURE_THRESHOLD * len(inputList)
		fails = 0
		for word in inputList:
			if not twl.check(word.lower()):
				fails += 1
		if fails < failRate: return input1

def filterIgnoreSpace(function,cipher,sortedShiftList):
	'''
	Runs recursiveCheck against a list of possible inputs with a function and returns a properly spaced string
	and the correct inputs

	>>> filterIgnoreSpace(lambda x, a, b: a*(x - b), "NGG NPX NGQ NJA", [(5,1),(2,4),(1,13)])
	'attack at dawn' 
	'''
	for param in sortedShiftList:
		input1 = shiftLinear(function,cipher,param[0],param[1]).replace(" ","")
		solution,output = recursiveCheck(input1,0,1)
		if solution:
			return (output,param)
def recursiveCheck(list1,index=0,length=1,partialSolution=''):
	'''
	Checks an input recursively against a scrabble dictionary (or 'a','i','o').
	The input must have no spaces - so string.replace(" ","") should be used on the input.
	In most cases it is better to use filterIgnoreSpace than recursiveCheck

	>>> solution = "att ack atd awn" 
	>>> recursiveCheck(solution.replace(" ",""))
	(True, 'attack at dawn')
	'''
	ONE_LETTER_WORDS = ['a','i','o']
	word = list1[index:index+length]
	longerWord = list1[index:index+length+1]
	nextWord = list1[index+length:index+length+1]
	if twl.check(word) or word in ONE_LETTER_WORDS:
		if index+length > len(list1) - 1:
			return True,(partialSolution+word)
		elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
			# TODO: find more elegant way of recursing
			longer,partL = recursiveCheck(list1,index,length+1,partialSolution)
			next,partN = recursiveCheck(list1,index+length,1,partialSolution+word+" ")
			if longer: return longer,partL
			else: return next,partN
		else: 
			return recursiveCheck(list1,index+length,1,partialSolution+word+" ")
	elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
		if index+length > len(list1) - 1: 
			return False,""
		return recursiveCheck(list1,index,length+1,partialSolution)
	else: 
		return False,""

def keyFind(cipher):
	words = set(twl.iterator())
	for word in words:
		print(word)
