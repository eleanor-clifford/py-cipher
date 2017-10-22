#!/bin/env python3
import file,core,substitution as s
__debug = False

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


frequency = core.frequencyList(cipher)
print("Letter Frequency")
[print(chr(i+65),": ",j,sep="") for i,j in enumerate(frequency)]

length = len(cipher)
divisors = [x for x in range(1,length+1) if length % x == 0]
print("Divisors:",end=" ")
[print(a,end=" ") for a in divisors]
print()