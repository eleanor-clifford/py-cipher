'''
'''
from collections import namedtuple , Counter
import numpy as np
import core,file
def pattern(word):
	pattern = np.zeros(len(word),dtype="int")
	index = 0
	seen = ""
	for i,letter in enumerate(word):
		if not letter in seen:
			if i == len(word) - 1: continue
			pattern[i] = index
			for j,nextLetter in enumerate(word[i+1:]):
				if letter == nextLetter:
					#print(i,j)
					pattern[i] = index
					pattern[j+i+1] = index
			index += 1
	return pattern

def toTupleArray(cipher):
	wordList = cipher.split(bytes([ord(" ")]))
	array = np.empty(len(wordList),dtype=tuple)
	wordTuple = namedtuple('wordTuple','word original length solved pattern')
	for i,j in enumerate(wordList):
		array[i] = wordTuple(word=bytearray(j),original=j,length=len(j),solved=np.array([False]*len(j)),pattern=pattern(j))
	return array

def scrap(tupleArray):
	for word in tupleArray:
		word.word = word.original
		for i in word.solved: i = False

def wordPossibilities(plaintext,tupleArray):
	possibilities = []
	for word in tupleArray:
		if np.array_equal(word.pattern,pattern(plaintext)): 
			possibilities.append(word.word)
	count = Counter(possibilities)
	possibilities = sorted(possibilities, key=lambda x: -count[x])
	sortedP = []
	for i in possibilities: 
		if not i in sortedP: sortedP.append(i)
	return sortedP

class cipherAlphabet:
	current = np.zeros(26,dtype="object")
	def __init__(self): 
		for i,letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
			self.current[i] = [letter,False]		
	nowhere = []
	duplicate = []
	def set(self,plain,cipher):
		index = np.where(self.current==[cipher,False])
		print(index)
		print(self.current[index])
		self.current[index][0] = plain
		self.current[index][1] = True
	
# def __init__(self): raise NotImplementedError
def shift(ciphertext,plaintext,tupleArray):
	for cipher,plain in zip(ciphertext,plaintext):
		for word in tupleArray:
			for i,letter in word.word:
				if letter == cipher and solved[i] == False:
					word.word[i] == plain
					word.solved[i] == true 



def partialCheck(tupleArray):
	for word in tupleArray:
		if word.length == 1 and word not in [bytes([ord("a")]),bytes([ord("i")]),bytes([ord("o")])]: return False
		elif not (False in word.solved and twl.check(word.word,"utf-8")): return False
	return True