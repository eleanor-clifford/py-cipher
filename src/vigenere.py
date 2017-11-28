try: import core, file
except ImportError: from src import core,file 
import string

def friedman():
	ciphertext = file.openAsAscii("cipher.txt")
	kp = 0.067
	kr = 1/26
	N = sum(core.frequencyList(ciphertext))
	#print(N)
	ko = sum([n*(n-1) for n in core.frequencyList(ciphertext)])/(N*(N-1))
	#print(ko)
	#print(sum(core.frequencyList(ciphertext)))
	keylength = (kp-kr)/(ko-kr)

	return (keylength)
def decrypt(keyword = bytearray("TEST","ascii"),ciphertext = file.openAsAscii("cipher.txt")):
	#print(keyword)
	#keyword = keyword.upper()
	index = 0
	solved = ""
	#print(ciphertext)
	for i in ciphertext:
		#print(chr(i), end = " ")
		if 65 <= i <= 90: 
			solved += chr((i - keyword[index])%26 + 65)
			index = (index+1)%(len(keyword))
		else:
			solved += chr(i)
	with open("output.txt","w") as f: print(solved,file=f)
	return solved



def kasiski(ciphertext = file.openAsAscii("cipher.txt")):
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
					#print(ciphertext[i:j+1])
					#print(len("".join(ciphertext[i:j+1]).replace("\n","")))
					diffs.add(len("".join(ciphertext[i:j+1]).replace("\n","")))
	#print(diffs)
	factors = []
	for i in range(2,int(max(diffs)/2)):
		a = ([n%i == 0 for n in diffs])
		if a.count(True) > len(a)*3/4: factors.append(i)
	#print(factors)
	#factors = set([x for _,x in sorted([(factors.count(a),a) for a in factors])])
	return factors,matches

def kasiskiNoSpace(ciphertext = file.openAsAscii("cipher.txt")):
	ciphertext = str(ciphertext,"ascii")
	translator = str.maketrans('', '', string.punctuation)
	ciphertext = ciphertext.translate(translator).replace(" ","")
	diffs = set()
	matches = 0
	for wordlen in range(7,20):
		for wordIndex in range(len(ciphertext)-wordlen):
			for word2Index in range(wordIndex+wordlen,len(ciphertext) - wordlen):
				word,word2 = ciphertext[wordIndex:wordIndex+wordlen],ciphertext[word2Index:word2Index+wordlen]
				if word == word2:
					print(word,word2,wordIndex,word2Index)
					matches += 1
					diffs.add(word2Index - wordIndex)
	#print(diffs)
	factors = []
	for i in range(2,int(max(diffs)/2)):
		a = ([n%i == 0 for n in diffs])
		if a.count(True) > len(a)*3/4: factors.append(i)
	#print(factors)
	#factors = set([x for _,x in sorted([(factors.count(a),a) for a in factors])])
	return factors,matches

def freqAnalysis(length=7, ciphertext = file.openAsAscii("cipher.txt")):
	translator = str.maketrans('', '', string.punctuation)
	ciphertext = bytearray(str(ciphertext,"ascii").translate(translator).replace(" ","").replace("\n",""),"ascii")
	split = []
	for i in range(length):
		split.append(bytearray([l for j,l in enumerate(ciphertext) if j%length == i]))
	keyword = bytearray([])
	#with open("splits.txt","w"): pass
	for i in split:
		open("splits.txt","a").write(str(i,"utf-8")+"\n")
		keyword.append(core.sortLinear(lambda x, a, b: a*(x-b), i, [1], range(26), core.frequencyList(ciphertext))[0][1]+97)
	open("splits.txt","a").write("\n")
	return str(keyword,"utf-8")

def align(splits=[a[:-1] for a in open("splits.txt").readlines()]):
	#print(splits[0])
	baseFrequency = core.frequencyList(bytearray(splits[0],"ascii"))
	#print(baseFrequency)
	shifts = []
	for i in splits:
		#print(i)
		frequency = core.frequencyList(bytearray(i,"ascii"))
		#print(frequency)
		shiftPossibility = []
		for shift in range(26):
			tempPossibility = 0
			for j in range(26):
				#print(frequency[((j+shift)%26)])
				tempPossibility += baseFrequency[j] * frequency[((j+shift)%26)]

			shiftPossibility.append((tempPossibility,shift))
		shifts.append(sorted(shiftPossibility,reverse=True)[0][1])
		#print(shiftPossibility)
	return str(bytes([shift + 97 for shift in shifts]))

		#print(max(meanFrequency))
		#meanFrequency = [100 * (a / sum(meanFrequency)) for a in meanFrequency]
		#alpha = "abcdefghijklmnopqrstuvwxyz"
		#ticks = ([x for _,x in reversed(sorted(zip(frequency,alpha)))])
		#frequency = frequency[-9:] + frequency[:-9]
		#print([(2*a + b)/3 for a,b in zip(meanFrequency,frequency)])

#print(kasiski())
#print(friedman())
#print(freqAnalysis())
#print(align())
#print(decrypt(keyword = bytearray("ESULLIH","ascii")))