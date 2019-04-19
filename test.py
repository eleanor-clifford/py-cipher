import string
try: from src import file
except ImportError: import file

ciphertext = file.openAsAscii("/home/el/Projects/py-cipher/cipher.txt")
translator = str.maketrans('', '', string.punctuation)
ciphertext = bytearray(str(ciphertext,"ascii").translate(translator).replace("\n",""),"ascii")
[print(chr(len(ciphertext.split()[i])+len(ciphertext.split()[i+1])+97),end=" ") for i in range(0,len(ciphertext.split())-2,2)]


