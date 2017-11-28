'''
'''
from src.TWL06 import twl

def shift(cipher,cipherAlphabet,utf8=False):
	cipher = cipher.lower()
	if utf8:
		decrypted = ""
		normalAlphabet = "abcdefghijklmnopqrstuvwxyz"
		for letter in cipher:
			try:
				decrypted += normalAlphabet[cipherAlphabet.index(letter)]
			except ValueError: decrypted += letter
	else:
		decrypted = bytearray("","ascii")
		normalAlphabet = bytearray("abcdefghijklmnopqrstuvwxyz","ascii")
		for letter in cipher:
			try:
				decrypted += bytes([normalAlphabet[cipherAlphabet.index(letter)]])
			except ValueError: decrypted += bytes([letter])
	return decrypted

def fixDouble(alphabet,utf8=False):
	if utf8: adjusted = ""
	else: adjusted = bytearray("","ascii")
	for i,letter in enumerate(alphabet):
		canAdd = True
		for last in range(i):
			if alphabet[last] == letter: canAdd = False
		if canAdd: 
			if utf8: adjusted += letter
			else: adjusted += bytes([letter])
	return adjusted
