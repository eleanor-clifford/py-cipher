'''
'''
from TWL06 import twl
def findKeyword(frequencyList):
	letterOrder = [4,19,0,14,8,13,18,7,17,3,11,2,20,12,22,5,6,24,15,1,21,10,9,23,16,25]
	cipherLetterOrder = [x for _,x in sorted(zip(frequencyList,range(26)))]
	cipherLetterOrder.reverse()
	newAlphabet = [x for _,x in sorted(zip(letterOrder,cipherLetterOrder))]
	newAlphabetString = ""
	for a in newAlphabet:
		newAlphabetString += chr(a+97)
	return newAlphabetString

def shift(cipher,cipherAlphabet):
	cipher = cipher.lower()
	decrypted = ""
	normalAlphabet = "abcdefghijklmnopqrstuvwxyz"
	for letter in cipher:
		try:
			decrypted += normalAlphabet[cipherAlphabet.index(letter)]
		except ValueError: decrypted += letter
	return decrypted
	

def fixDouble(alphabet):
	adjusted = ""
	for i in range(len(alphabet)):
		canAdd = True
		for last in range(i):
			if alphabet[last] == alphabet[i]: canAdd = False
		if canAdd: adjusted += alphabet[i]
	return adjusted

def alphabetBuilder(cipher, possiblePhrase):
	raise NotImplementedError