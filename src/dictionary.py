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
try:
	from src.TWL06 import twl
	from src.core import shiftLinear
except ImportError:
	from TWL06 import twl
	from core import shiftLinear
__debug = True

def filterIgnoreSpace(function,cipher,sortedShiftList,utf8=False):
	'''
	Runs recursiveCheck against a list of possible inputs with a function and returns a properly spaced string
	and the correct inputs

	>>> filterIgnoreSpace(lambda x, a, b: a*(x - b), "NGG NPX NGQ NJA", [(5,1),(2,4),(1,13)],utf8=True)
	('attack at dawn', (1, 13)) 
	>>> filterIgnoreSpace(lambda x, a, b: a*(x - b), bytearray("NGG NPX NGQ NJA","ascii"), [(5,1),(2,4),(1,13)])
	('attack at dawn', (1, 13))
	'''
	for param in sortedShiftList:
		input1 = shiftLinear(function,cipher,param[0],param[1],utf8=utf8)
		if utf8: solution,output = recursiveCheck(input1.replace(" ",""))
		else: solution,output = recursiveCheck(str(input1,"utf-8").replace(" ",""))
		if solution:
			return (output,param)
def recursiveCheck(cipher,index=0,length=1,partialSolution=''):
	'''
	Checks an input recursively against a scrabble dictionary (or 'a','i','o').
	The input must have no spaces - so string.replace(" ","") should be used on the input.
	In most cases it is better to use filterIgnoreSpace than recursiveCheck

	>>> solution = "att ack atd awn" 
	>>> recursiveCheck(solution.replace(" ",""))
	(True, 'attack at dawn')
	'''
	ONE_LETTER_WORDS = ['a','i','o']
	word = cipher[index:index+length]
	longerWord = cipher[index:index+length+1]
	nextWord = cipher[index+length:index+length+1]
	if twl.check(word) or word in ONE_LETTER_WORDS:
		if index+length > len(cipher) - 1:
			return True,(partialSolution+word)
		elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
			# TODO: find more elegant way of recursing
			longer,partL = recursiveCheck(cipher,index,length+1,partialSolution)
			next,partN = recursiveCheck(cipher,index+length,1,partialSolution+word+" ")
			if longer: return longer,partL
			else: return next,partN
		else: 
			return recursiveCheck(cipher,index+length,1,partialSolution+word+" ")
	elif twl.check(longerWord) or len(twl.children(longerWord)) > 0:
		if index+length > len(cipher) - 1: 
			#print(partialSolution)
			return True,(partialSolution+word)
		return recursiveCheck(cipher,index,length+1,partialSolution)
	else: 
		#print(partialSolution)
		return False,""

def partialCheck(): raise NotImplementedError

