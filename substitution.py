'''
'''
from collections import namedtuple , Counter
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
	nowhere = []
	duplicate = []
	found = []
	def set(self,plaintext,ciphertext):
		done = bytearray("","ascii")
		### CHECK:
		for plain,cipher in zip(plaintext,ciphertext):
			for p,c in self.found:
				for i,j in zip(p,c):
					if (i == plain) ^ (j == cipher):
						#print(chr(i),chr(j),"XOR",chr(plain),chr(cipher))
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



def partialCheck(tupleArray):
	for word in tupleArray.array:
		if word.length == 1 and word.solved[0] == True and word[0] not in bytearray("aio","ascii"): return False
		elif not (False in word.solved) and not (twl.check(str(word.word,"utf-8")) or word.word in bytearray("aio","ascii")): 
			return False
	return True

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
			if partialCheck(tupleArray):
				alphabet.found.append((word,solution))
				maybeReturn = recursiveSolve(words[1:],tupleArray,accepted + [(word,solution)],recursionCounter+1)
				if maybeReturn: 
					return maybeReturn
