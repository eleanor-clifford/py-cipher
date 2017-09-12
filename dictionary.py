'''
Depends on shiftLinear from core
'''
import twl
from core import shiftLinear


def filter(function,cipher,sortedShiftList): # last is tuple 
	FAILURE_THRESHOLD = 0.2
	for param in sortedShiftList:
		print(param)
		input1 = shiftLinear(function,cipher,param[0],param[1])
		inputList = input1.split()
		failRate = FAILURE_THRESHOLD * len(inputList)
		fails = 0
		for word in inputList:
			if not twl.check(word.lower()):
				fails += 1
		if fails < failRate: return input1

def filterIgnoreSpace(function,cipher,sortedShiftList):
	for param in sortedShiftList:
		input1 = shiftLinear(function,cipher,param[0],param[1])
		solution,output = recursiveCheck(input1,0,1)
		if solution:
			return (output,param)
def recursiveCheck(list1,index,length,partialSolution=''):
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
