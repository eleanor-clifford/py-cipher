try: import core, file
except ImportError: from src import core,file 
import string

def friedman(ciphertext):
	'''
	Not tested whatsoever
	'''
	kp = 0.067
	kr = 1/26
	N = sum(core.frequencyList(ciphertext))
	ko = sum([n*(n-1) for n in core.frequencyList(ciphertext)])/(N*(N-1))
	keylength = (kp-kr)/(ko-kr)

	return (keylength)
def decrypt(keyword,ciphertext):
	index = 0
	solved = ""
	for i in ciphertext:
		open("log.txt","a").write(chr(i))
		#print(chr(i), end = " ")
		if 97 <= i <= 122:
			i -= 32
		if 65 <= i <= 90: 
			open("log.txt","a").write("yay")
			solved += chr((i - keyword[index])%26 + 65)
			index = (index+1)%(len(keyword))
		else:
			solved += chr(i)
	with open("output.txt","w") as f: print(solved,file=f)
	return solved



def kasiski(ciphertext):
	ciphertext = str(ciphertext,"ascii")
	translator = str.maketrans('', '', string.punctuation)
	ciphertext = ciphertext.translate(translator).split()
	diffs = set()
	matches = 0
	for i,word in enumerate(ciphertext):
		if len(word) > 3:
			for j,word2 in enumerate(ciphertext[i+1:],start=i):
				if word == word2: 
					print(word,word2,i,j)
					matches += 1
					diffs.add(len("".join(ciphertext[i:j+1]).replace("\n","")))
	factors = []
	print(diffs)
	for i in range(2,int(max(diffs)/2)):
		a = ([n%i == 0 for n in diffs])
		if a.count(True) > len(a)*3/4: factors.append(i)
	return factors,matches

def kasiskiNoSpace(ciphertext):
	try: ciphertext = str(ciphertext,"ascii")
	except: pass
	translator = str.maketrans('', '', string.punctuation)
	ciphertext = ciphertext.translate(translator).replace(" ","")
	diffs = set()
	matches = 0
	for wordlen in range(9,12):
		for wordIndex in range(len(ciphertext)-wordlen):
			for word2Index in range(wordIndex+wordlen,len(ciphertext) - wordlen):
				word,word2 = ciphertext[wordIndex:wordIndex+wordlen],ciphertext[word2Index:word2Index+wordlen]
				if word == word2:
					print(word,word2,wordIndex,word2Index)
					matches += 1
					diffs.add(word2Index - wordIndex)
	factors = []
	if diffs == set(): return [[],0]
	for i in range(2,int(max(diffs)/2)):
		a = ([n%i == 0 for n in diffs])
		if a.count(True) > len(a)*5/6: factors.append(i)
	return factors,matches

def freqAnalysis(length, ciphertext):
	translator = str.maketrans('', '', string.punctuation)
	ciphertext = bytearray(str(ciphertext,"ascii").translate(translator).replace(" ","").replace("\n",""),"ascii")
	split = []
	for i in range(length):
		split.append(bytearray([l for j,l in enumerate(ciphertext) if j%length == i]))
	keyword = bytearray([])
	for i in split:
		open("splits.txt","a").write(str(i,"utf-8")+"\n")
		keyword.append(core.sortLinear(lambda x, a, b: a*(x-b), i, [1], range(26), core.frequencyList(ciphertext))[0][1]+97)
	open("splits.txt","a").write("\n")
	return str(keyword,"utf-8")

def align(splits):
	baseFrequency = core.frequencyList(bytearray(splits[0],"ascii"))
	shifts = []
	for i in splits:
		frequency = core.frequencyList(bytearray(i,"ascii"))
		shiftPossibility = []
		for shift in range(26):
			tempPossibility = 0
			for j in range(26):
				tempPossibility += baseFrequency[j] * frequency[((j+shift)%26)]
			shiftPossibility.append((tempPossibility,shift))
		shifts.append(sorted(shiftPossibility,reverse=True)[0][1])
	return str(bytes([shift + 97 for shift in shifts]))