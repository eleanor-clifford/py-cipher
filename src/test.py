import file
ciphertext = str(file.openAsAscii("cipher.txt"),"utf-8").replace(" ","")
matches = 0
diffs = set()
for wordlen in range(7,10):
	for wordIndex in range(len(ciphertext)-wordlen):
		for word2Index in range(wordIndex+wordlen,len(ciphertext) - wordlen):
			word,word2 = ciphertext[wordIndex:wordIndex+wordlen],ciphertext[word2Index:word2Index+wordlen]
			if word == word2:
				print(word,word2,wordIndex,word2Index)
				matches += 1
				diffs.add(word2Index - wordIndex)
print(diffs)