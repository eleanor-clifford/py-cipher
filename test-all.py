#!/usr/bin/env python3
# *-* coding: iso-8859-1 *-*
''' 
Uses the core and dictionary modules to test for Affine ciphers (includes Caesar and Atbash)

Sample Usage
$ ./test-all.py
ZGG ZXP ZGW ZDM
AFFINE TEST...SUCCESS
D(x): x -> 25(x-11) mod 26
The plaintext has been output to output.txt
Show output? y
attack at dawn

$ ./test-all.py
TSCRC RPFBY WKQAI CMSBQ
AFFINE TEST...FAILED
MONOALPHABETIC SUBSTITUTION TEST...FAILED
KEYWORD TEST...SUCCESS
The plaintext has been output to output.txt
Keyword is pliablenesses
Show output? y
this is a keyword cipher

'''
__debug = True

import core, dictionary, key, file, substitution as s
import copy, string
from TWL06 import twl

# see https://stackoverflow.com/questions/12586601/remove-last-stdout-line-in-python
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

if __debug: path = ""
else: path = input("Enter path of file to read from (cipher.txt): ")
if path == "": path = "cipher.txt"
print(CURSOR_UP_ONE+ERASE_LINE+"\r",end="")
try:
	cipher = file.openAsAscii(path)
	print("Reading from",path+"...")
except FileNotFoundError: 
	cipher = bytes(input("File not found. Enter cipher:\n"),"ascii")
	print(CURSOR_UP_ONE+ERASE_LINE+CURSOR_UP_ONE+ERASE_LINE+"\r"+str(cipher,"utf-8"))
out = open("output.txt","w")
log = open("errorlog.txt","w")

translator = str.maketrans('', '', string.punctuation)
cipher = bytearray(str(cipher,"utf-8").translate(translator),"ascii")
COPRIMES = [1,3,5,7,9,11,15,17,19,21,23,25] # coprimes of 26 - the modular multiplicative inverse is the same set
f = core.frequencyList(cipher)
print("AFFINE TEST...",end="")
affineShiftList = core.sortLinear(lambda x, a, b: a*(x - b), cipher, COPRIMES, range(26), f)
affine = dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b),cipher,affineShiftList)
if affine: 
	print("SUCCESS")
	print(affine[0],file=out)
	print("D(x): x -> ",affine[1][0],"(x","-",affine[1][1],") mod 26",sep="")
	print("The plaintext has been output to output.txt")
	try:
		if input("Show output? ")[0] == 'y': print(affine[0])
	except IndexError: pass
else:
	try:
		print("FAILED")
		print("MONOALPHABETIC SUBSTITUTION TEST...")
		if __debug: cribs = ['harry,']
		else: cribs = input("Please enter any cribs you know: ").split()
		inputArray = cribs + ['the','and']
		tupleArray = s.tupleArray(cipher)
		sol = s.recursiveSolve(inputArray,tupleArray)
		alphabet = s.cipherAlphabet()
		for i,j in sol:
			alphabet.set(i,j)
		s.shift(alphabet,tupleArray)
		tupleArray = s.recursiveGuess(tupleArray,alphabet,minWord=6)
		s.shift(alphabet,tupleArray)
		alphabet = s.finalCheck(tupleArray,alphabet)
		s.shift(alphabet,tupleArray)
		tupleArray.show()
		alphabet.show()

		a = input("Enter any more letters you can see (or enter to fill alphabetically, x to proceed to the next text)").split()
		print(a,file=log)
		if len(a) > 0 and a[0].lower()[0] == 'x': raise Exception
		if len(a) == 2:
			alphabet.set(bytearray(a[0],"ascii"),bytearray(a[1],"ascii"))
			if input("Fill also? ")[0] == 'y':
				alphabet.fill()
		else:
			alphabet.fill()
		s.shift(alphabet,tupleArray)
		tupleArray.show(file=out)
		alphabet.show()
		print("The plaintext has been output to output.txt")
	except Exception as e:
		print("Unexpected Error in MAS Test:", e, file=log, flush=True) 	
		print(CURSOR_UP_ONE+ERASE_LINE+"\r"+CURSOR_UP_ONE+ERASE_LINE+"\rMONOALPHABETIC SUBSTITUTION TEST...FAILED")
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
					
#		else:
#			print("FAILED")
#			print("RANDOM KEY TEST...")
#			MAX_LENGTH = 4
#			for length in range(1,MAX_LENGTH):
#				if length > 1: 
#					print("FAILED")
#				print("\t",length,"LETTER WORDS...",end="",flush=True)
#				for x in range(26**length):
#					output = ""
#					while x > 0:
#						output += chr(97+x%26)
#						x = x//26
#					cipherAlphabet = key.fixDouble(bytearray(output[::-1] + "abcdefghijklmnopqrstuvwxyz","ascii"))
#					decrypted = key.shift(cipher,cipherAlphabet)
#					keyword = dictionary.recursiveCheck(str(decrypted,"utf-8").replace(" ",""))
#					if keyword[0]:
#						print("SUCCESS")
#						print("is",keyword[1],"english? ",end="")
#						if input()[0] == 'y':
#							print("Keyword is",word)
#							break
#						else:
#							print("RANDOM KEY TEST...",end="",flush=True)