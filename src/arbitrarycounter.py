import string
try: from src import file
except ImportError: import file

ciphertext = file.openAsAscii("/home/el/Projects/py-cipher/cipher.txt")
translator = str.maketrans('', '', string.punctuation)
ciphertext = bytearray(str(ciphertext,"ascii").translate(translator).replace(" ","").replace("\n",""),"ascii")

N = 2
slide = False
count = [["&",0]]
if slide:
	for i in range(len(ciphertext) - N):
		char = ciphertext[i:i+N]
		fst = [i for _,i in count]
		if char in fst:
			count[fst.index(char)][0] += 1
		else:
			count.append([1,char])
else:
	for i in range(0,len(ciphertext) - N,N):
		char = ciphertext[i:i+N]
		fst = [i for _,i in count]
		if char in fst:
			count[fst.index(char)][0] += 1
		else:
			count.append([1,char])

[print([chr(i) for i in x],j/sum(list(zip(*count))[0][1:])) for j,x in sorted(count[1:])]