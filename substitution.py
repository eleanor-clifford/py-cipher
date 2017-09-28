'''
'''
from collections import namedtuple , Counter
import copy
import numpy as np
import core,file
from TWL06 import twl
def pattern(word,utf8=False):
	pattern = np.zeros(len(word),dtype="int")
	index = 0
	if utf8: seen = ""
	else: seen = bytearray("","ascii")
	for i,letter in enumerate(word):
		try: 
			if not letter in seen:
				pattern[i] = index
				for j,nextLetter in enumerate(word[i+1:]):
					if letter == nextLetter:
						pattern[i] = index
						pattern[j+i+1] = index
				seen.append(letter)
				index += 1
		except TypeError: 
			print("ERROR: Check that the input is a bytearray, or utf8=True is set")
			return
	return pattern

class tupleArray:
	array = np.empty([])
	def __init__(self,cipher):
		wordList = cipher.split(bytes([ord(" ")]))
		self.array = np.empty(len(wordList),dtype=tuple)
		wordTuple = namedtuple('wordTuple','word original length solved pattern')
		for i,j in enumerate(wordList):
			self.array[i] = wordTuple(word=bytearray(j),original=j,length=len(j),solved=np.array([False]*len(j)),pattern=pattern(j))
	def show(self):
		for word in self.array:
			for j,letter in enumerate(word.word):
				if word.solved[j]: print(chr(letter).lower(),end="")
				else: print(chr(letter).upper(),end="")
			print(" ",end="")
		print("\n",end="")
	def scrap(self):
		for word in self.array:
			for i in range(len(word.word)): word.word[i] = word.original[i]
			for i in range(len(word.solved)): word.solved[i] = False
	def simpleCheck(self):
		for word in self.array:
			if word.length == 1 and word.solved[0] == True and word[0] not in bytearray("aio","ascii"): return [False,word]
			elif not (False in word.solved) and not (twl.check(str(word.word,"utf-8")) or word.word in bytearray("aio","ascii")): 
				return [False,word]
		return [True,bytearray("","ascii")]
	def fullCheck(self):
		for word in self.array:
			for bool in word.solved:
				if not bool: return False
		return True

def wordPossibilities(plaintext,tupleArray):
	possibilities = []
	for word in tupleArray.array:
		if np.array_equal(word.pattern,pattern(plaintext)): 
			possibilities.append(str(word.original,"utf-8"))
	count = Counter(possibilities)
	possibilities = sorted(possibilities, key=lambda x: -count[x])
	sortedP = []
	for i in possibilities: 
		i = bytearray(i.lower(),"ascii")
		if not i in sortedP: sortedP.append(i)
	return sortedP

class cipherAlphabet:
	current = np.zeros(26,dtype="object")
	def __init__(self): 
		for i,letter in enumerate(bytearray("abcdefghijklmnopqrstuvwxyz","ascii")):
			self.current[i] = [letter,False]		
	found = []

	def show(self):
		for i in range(26): print(chr(65+i),end=" ")
		print()
		for i in self.current:
			if i[1]:
				print(chr(i[0]),end=" ")
			else: print(" ",end=" ")
		print()
	def set(self,plaintext,ciphertext):
		done = bytearray("","ascii")
		### CHECK:
		for plain,cipher in zip(plaintext,ciphertext):
			for p,c in self.found:
				for i,j in zip(p,c):
					if (i == plain) ^ (j == cipher):
						print(plaintext,ciphertext)
						print(chr(i),chr(j),"XOR",chr(plain),chr(cipher))
						return 1
		### CHANGE:
		for plain,cipher in zip(plaintext,ciphertext):

			index = (cipher-97)%26
			if not self.current[index][1]:
				self.current[index][0] = plain
				self.current[index][1] = True
				done += bytes([cipher])					
			else: 
				if cipher in done: continue
				else: print("WARNING:",cipher,"is not a letter or has already been set")
	def scrap(self):
		for i,letter in enumerate(self.current):
			if letter[1]: 
				self.current[i] = [i+97,False]

# def __init__(self): raise NotImplementedError
def shift(alphabet,tupleArray):
	for cipher,plain in enumerate(alphabet.current):
		#print(plain,cipher)
		if plain[1]:
			cipher += 65
			plain = plain[0]
			for word in tupleArray.array:
				for i,letter in enumerate(word.word):
					if letter == cipher and word.solved[i] == False:
						word.word[i] = plain
						word.solved[i] = True 





def recursiveSolve(words, tupleArray, accepted=[], recursionCounter = 0): # returns tupleArray
	'''
	It will recursively try all inputs given to it against all 
	possibilities in the text, depending on repeated letter patterns, 
	and return a list of completed words, as (plaintext, ciphertext) tuples


	>>> from substitution import recursiveSolve, tupleArray
	>>> t = tupleArray(bytearray("JL NJIWI","ascii"))
	>>> recursiveSolve(['hi','there'],t)
	[(bytearray(b'hi'), bytearray(b'jl')), (bytearray(b'there'), bytearray(b'njiwi'))]
	>>> t.show()
	hi there
	'''
	if len(words) == 0: return accepted
	word = bytearray(words[0],"ascii")
	alphabet = cipherAlphabet()
	if recursionCounter == 0: alphabet.found += (accepted)
	for i,solution in enumerate(wordPossibilities(word,tupleArray)):
		tupleArray.scrap()
		alphabet.scrap()
		for plain,cipher in accepted: alphabet.set(plain,cipher)
		if alphabet.set(word,solution) == 1: 
			continue
		else: 
			shift(alphabet,tupleArray)
			if tupleArray.simpleCheck()[0]:
				alphabet.found.append((word,solution))
				maybeReturn = recursiveSolve(words[1:],tupleArray,accepted + [(word,solution)],recursionCounter+1)
				if maybeReturn: 
					return maybeReturn
def flatten(L):
	if L == None: yield None
	for item in L:
		if type(item) == type(bytearray("","ascii")):
			yield item
		else: yield from flatten(item)
def recursiveGuess(masterArray,alphabet,minWord=6,failCount=0,newWords=[]):
	print(newWords)
	tupleArray = copy.deepcopy(masterArray)
	if tupleArray.fullCheck(): return tupleArray
	unknowns = []
	for word in tupleArray.array:
		if word.length < minWord: continue
		print(word.word)
		#print(word,alphabet)
		possibles = recursiveCheck(word,alphabet)
		if possibles == None: continue
		for test in flatten([possibles]):
			if test == word.word: 
				break
			elif alphabet.set(test,word.original.lower()) == 1: 
				print("WTF",test,word.original)
				continue
			else:
				shift(alphabet,tupleArray)
				print("shifted",test,word.word)
				check = tupleArray.simpleCheck()
				if not check[0] and not check[1].word in newWords:
					if input("is "+str(check[1].word)+" a word? ")[0] == 'y': 
						newWords += check[1].word
						check[0] = True
					else:
						tupleArray = copy.deepcopy(masterArray)
						continue
				if check[0]:
					a = recursiveGuess(tupleArray,alphabet,minWord,failCount,newWords)
					if a: 
						return a
					else: 
						failCount += 1
						print("FAIL",word)
						break
						#return tupleArray

		else: 
			print("FUCK")
			return masterArray
	


def recursiveCheck(masterTuple,alphabet,found=None):
	wordTuple = copy.deepcopy(masterTuple)
	returnValue = []
	if found:
		for i in range(len(wordTuple.word)):
			if wordTuple.word[i] == wordTuple.original[found[0]] and wordTuple.solved[i] == False: 
				wordTuple.word[i] = found[1]
				wordTuple.solved[i] = True
	start = bytearray("","ascii")
	index = 0
	for i,letter in enumerate(wordTuple.word):
		if wordTuple.solved[i] == True:
			start += bytes([letter])
		else: 
			index = i
			break
	if len(start) == 0: return None
	if len(start) == wordTuple.length: 
		if twl.check(str(wordTuple.word,'utf-8')): return wordTuple.word
		else: return None
	for possible in twl.children(str(start,"utf-8")):
		if possible == '$': continue
		for plain,_ in alphabet.found:
			if ord(possible) in plain: break
		else:
			a = recursiveCheck(wordTuple,alphabet,(index,ord(possible)))
			if a: returnValue.append(a)
	return returnValue
	