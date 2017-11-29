from src import core, dictionary, substitution as s, hill as h
from src.TWL06 import twl
import tkinter as tk
import string

# see https://stackoverflow.com/questions/12586601/remove-last-stdout-line-in-python
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

log = open("errorlog.txt","w")
def affine(cipher):
	translator = str.maketrans('', '', string.punctuation)
	cipher = bytearray(str(cipher,"utf-8").translate(translator),"ascii")
	COPRIMES = [1,3,5,7,9,11,15,17,19,21,23,25] # coprimes of 26 - the modular multiplicative inverse is the same set
	f = core.frequencyList(cipher)
	affineShiftList = core.sortLinear(lambda x, a, b: a*(x - b), cipher, COPRIMES, range(26), f)
	affine = dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b),cipher,affineShiftList)
	if affine: 
		with open("output.txt","w") as out: print(affine[0],file=out)
		return True,affine[1][0],affine[1][1]
	else: return False,0,0
def mas(cipher, cribs):
	try:
		translator = str.maketrans('', '', string.punctuation)
		cipher = bytearray(str(cipher,"utf-8").translate(translator),"ascii")
		tupleArray = s.tupleArray(cipher)
		sol = s.recursiveSolve(cribs,tupleArray)
		alphabet = s.cipherAlphabet()
		for i,j in sol:
			alphabet.set(i,j)
		s.shift(alphabet,tupleArray)
		tupleArray = s.recursiveGuess(tupleArray,alphabet,minWord=6)
		s.shift(alphabet,tupleArray)
		alphabet = s.finalCheck(tupleArray,alphabet)
		s.shift(alphabet,tupleArray)
		with open("output.txt","w") as out: tupleArray.show(file=out)
		with open("alphabet.txt","w") as a: alphabet.show(file=a)
		return tupleArray,alphabet
	except Exception as e:
		print("Unexpected Error in MAS Test:", e, file=log, flush=True) 
def FinishMAS(plain, cipher, fill, tupleArray, alphabet):
	try:
		if not (plain == "" or cipher == ""): 
			alphabet.set(bytearray(plain,"ascii"),bytearray(cipher.lower(),"ascii"))
		if fill: alphabet.fill()
		#print(alphabet.current)
		s.shift(alphabet,tupleArray) 
		with open("output.txt","w") as out:
			tupleArray.show(file=out)
		with open("alphabet.txt","w") as a: alphabet.show(file=a)
	except Exception as e:
		print("Unexpected Error in MAS Test:", e, file=log, flush=True) 	

def keyword(cipher):
	print("KEYWORD TEST...",end="",flush=True)
	words = set(twl.iterator())
	for word in words:
		cipherAlphabet = key.fixDouble(bytearray(word + "abcdefghijklmnopqrstuvwxyz","ascii"))
		decrypted = key.shift(cipher,cipherAlphabet)
		keyword = dictionary.recursiveCheck(str(decrypted,"utf-8").replace(" ",""))
		if keyword[0]:
			print("is \"",keyword[1],"\" english? ",end="", sep="") 
			if input()[0] == 'y':
				print(CURSOR_UP_ONE+ERASE_LINE+"\rKEYWORD TEST...SUCCESS")
				print(keyword[1],file=out)
				print("The plaintext has been output to output.txt\nKeyword is "+word)
				try:
					if input("Show output? ")[0] == 'y': print(keyword[1])
				except IndexError: pass
				break
			else:
				print(CURSOR_UP_ONE+ERASE_LINE+"\rKEYWORD TEST...",end="",flush=True)
					
def hill(cipher):
	with open("output.txt","w") as out:
		flag = False
		for n in range(2,5):
			for i in h.frequencyAnalysisWithC(N=n,ciphertext=cipher):
				if i: 
					print(i,file=out)
					flag = True
		return flag
