'''
'''

__debug = False

from collections import namedtuple , Counter
import copy, sys
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
		wordList = cipher.strip().split(bytes([ord(" ")]))
		self.array = np.empty(len(wordList),dtype=tuple)
		wordTuple = namedtuple('wordTuple','word original length solved pattern')
		for i,j in enumerate(wordList):
			self.array[i] = wordTuple(word=bytearray(j),original=j,length=len(j),solved=np.array([False]*len(j)),pattern=pattern(j))
	def show(self,file=sys.stdout):
		for word in self.array:
			for j,letter in enumerate(word.word):
				if word.solved[j]: print(chr(letter).lower(),end="",file=file)
				else: print(chr(letter).upper(),end="",file=file)
			print(" ",end="",file=file)
		print("\n",end="",file=file)
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
	def show(self,file=sys.stdout):
		for i in range(26): print(chr(97+i),end=" ",file=file)
		output = np.zeros(26,dtype=int)
		for i,letter in enumerate(self.current):
			if letter[1]: output[letter[0] - 97] = i + 65
		print(file=file)
		for i in output:
			if i != 0:
				print(chr(i),end=" ",file=file)
			else: print(" ",end=" ",file=file)
		print(file=file)
	def set(self,plaintext,ciphertext):
		done = bytearray("","ascii")
		### CHECK:
		for plain,cipher in zip(plaintext,ciphertext):
			for p,c in self.found:
				for i,j in zip(p,c):
					if (i == plain) ^ (j == cipher):
						return 1
		### SET:
		for plain,cipher in zip(plaintext,ciphertext):
			if not (plaintext,ciphertext) in self.found:
				self.found.append((plaintext,ciphertext))
			index = (cipher-97)%26
			if not self.current[index][1]:
				self.current[index][0] = plain
				self.current[index][1] = True
				done += bytes([cipher])
		return 0					
	def scrap(self,found=False):
		for i,letter in enumerate(self.current):
			if letter[1]: 
				self.current[i] = [i+97,False]
		if found: self.found = []
	def fill(self):
		missingCipher = []
		for i,letter in enumerate(self.current):
			if not letter[1]: missingCipher.append(i+97)
		for plain in range(97,123):
			for i,cipher in enumerate(self.current):
				if cipher[0] == plain and cipher[1]: break
			else:
				self.set(bytes([plain]),bytes([missingCipher[0]]))
				missingCipher = missingCipher[1:]
		

def shift(alphabet,tupleArray):
	for cipher,plain in enumerate(alphabet.current):
		if plain[1]:
			cipher += 65
			plain = plain[0]
			for word in tupleArray.array:
				for i,letter in enumerate(word.word):
					if letter == cipher and word.solved[i] == False:
						word.word[i] = plain
						word.solved[i] = True 
	return 0





def recursiveSolve(words, tupleArray, accepted=[], recursionCounter = 0,newWords=[]):
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
	for i,solution in enumerate(wordPossibilities(word,tupleArray)):
		tupleArray.scrap()
		alphabet.scrap(found=True)
		for plain,cipher in accepted: alphabet.set(plain,cipher)
		if alphabet.set(word,solution) == 1: 
			continue
		else: 
			shift(alphabet,tupleArray)
			check = tupleArray.simpleCheck()
			if __debug: print(check[1])
			if not check[0] and check[1].word in newWords: check[0] = True
			if not check[0]:
				if __debug: bool = True
				else: bool = input("is "+str(check[1].word)+" a word? ")[0] == 'y'
				CURSOR_UP_ONE = '\x1b[1A'
				ERASE_LINE = '\x1b[2K'
				print(CURSOR_UP_ONE+ERASE_LINE+"\r",end="")
				if bool:
					twl.add(check[1].word)
					check[0] = True
					newWords.append(check[1].word)
			if check[0]: maybeReturn = recursiveSolve(words[1:],tupleArray,accepted + [(word,solution)],recursionCounter+1,newWords=newWords)
			else: 
				continue
			if maybeReturn: 
				return maybeReturn
def flatten(L):
	if L == None: yield None
	for item in L:
		if type(item) == type(bytearray("","ascii")):
			yield item
		else: yield from flatten(item)
def recursiveGuess(masterArray,alphabet,minWord=6,failCount=0,newWords=[]):
	tupleArray = copy.deepcopy(masterArray)
	if tupleArray.fullCheck(): return tupleArray
	unknowns = []
	for word in tupleArray.array:
		if word.length < minWord: continue
		possibles = recursiveCheck(word,alphabet)
		if possibles == None: continue
		for test in flatten([possibles]):
			if test == word.word: 
				break
			elif alphabet.set(test,word.original.lower()) == 1: 
				continue
			else:
				shift(alphabet,tupleArray)
				check = tupleArray.simpleCheck()
				if not check[0] and not check[1].word in newWords:
					if __debug: bool = True
					else: bool = input("is "+str(check[1].word)+" a word? ")[0] == 'y'
					CURSOR_UP_ONE = '\x1b[1A'
					ERASE_LINE = '\x1b[2K'
					print(CURSOR_UP_ONE+ERASE_LINE+"\r",end="")
					if bool:
						twl.add(check[1].word)
						check[0] = True
						newWords.append(check[1].word)
				if check[0]:
					a = recursiveGuess(tupleArray,alphabet,minWord,failCount,newWords)
					if a: 
						return a
					else: 
						failCount += 1
						break
				else:
					tupleArray = copy.deepcopy(masterArray)
					continue
	else: 
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
	

def finalCheck(tupleArray, alphabet): 
	'''
	This occurs when a letter is missed because it only occurs at the start of the word,
	where recursiveCheck misses it as it cannot be checked directly using twl
	'''
	for word in tupleArray.array:
		if (len(word.solved) > 1 and not word.solved[0]) and not ( False in word.solved[1:]):
			possible = []
			orig = word.word[0]
			for l in range(26):
				word.word[0] = l+97
				if twl.check(str(word.word,"utf-8")):
					possible.append((bytes([l+97]),bytes([orig+32])))
			if len(possible) == 1:
				alphabet.set(possible[0][0],possible[0][1])
			word.word[0] = orig
	return alphabet
