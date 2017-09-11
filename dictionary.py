'''
Depends on shiftLinearNoCheck from core
'''
import twl
from core import shiftLinearNoCheck


def filter(function,cipher,sortedShiftList): # last is tuple 
	FAILURE_THRESHOLD = 0.2
	for param in sortedShiftList:
		print(param)
		input1 = shiftLinearNoCheck(function,cipher,param[0],param[1])
		inputList = input1.split()
		failRate = FAILURE_THRESHOLD * len(inputList)
		fails = 0
		for word in inputList:
			if not twl.check(word.lower()):
				fails += 1
		if fails < failRate: return input1

def filterIgnoreSpace(function,cipher,sortedShiftList):
	for param in sortedShiftList:
		input1 = shiftLinearNoCheck(function,cipher,param[0],param[1])
		if recursiveCheck(input1,0,1):
			print(input1)
			return param
def recursiveCheck(list1,index,length):
	ONE_LETTER_WORDS = ['a','i','o']
	word = list1[index:index+length]
	longerWord = list1[index:index+length+1]
	nextWord = list1[index+length:index+length+1]
	if twl.check(word) or word in ONE_LETTER_WORDS:
		if index+length >= len(list1) - 1:
			return True
		elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
			return recursiveCheck(list1,index,length+1) or recursiveCheck(list1,index+length,1)
		else: 
			return recursiveCheck(list1,index+length,1)
	elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
		if index+length > len(list1) - 1: 
			return False
		return recursiveCheck(list1,index,length+1)
	else: 
		return False
