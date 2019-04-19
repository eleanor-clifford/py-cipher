import file
ciphertext = str(file.openAsAscii("cipher.txt"),"utf-8").replace(" ","")
matches = 0
diffs = set()
N=5
print(len(ciphertext)/N)
for wordlen in range(N*5,N*8,N):
	print("Wordlen: {0}".format(wordlen))
	for wordIndex in range(len(ciphertext)-wordlen):
		for word2Index in range(wordIndex+wordlen,len(ciphertext) - wordlen,N):
			word,word2 = ciphertext[wordIndex:wordIndex+wordlen:N],ciphertext[word2Index:word2Index+wordlen:N]
			if word == word2:
				print(word,word2,wordIndex,word2Index)
				matches += 1
				diffs.add(word2Index - wordIndex)
print(diffs)