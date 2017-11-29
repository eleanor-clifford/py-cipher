import numpy as np, string, math
from itertools import product, permutations
try: from src import matrices, file, dictionary, hillcwrapper
except ImportError: import matrices, file, dictionary, hillcwrapper

def solve(dkey, N, ciphertext):
	cipher3Vectors = np.empty(int(len(ciphertext)/N),dtype="object")
	for i in range(len(ciphertext)):
		try: 
			cipher3Vectors[i] = np.array([j - 65 for j in ciphertext[N*i:(N*i)+N]])
		except IndexError: pass
	cipher3VectorsSolved = np.empty(int(len(ciphertext)/N),dtype="object")
	if np.linalg.det(dkey) != 0:
		for i,j in enumerate(cipher3Vectors): 
			cipher3VectorsSolved[i] = np.dot(dkey,j)
		solved = ""
		for i in cipher3VectorsSolved:
			for j in np.array(i):
				d = int(j)%26 + 97
				solved += chr(d)
		if dictionary.recursiveCheck(solved[:10])[0]:
			return (dkey,solved)
		else: return

def frequencyAnalysisWithC(N, ciphertext):
	'''
	Runs in O(26^N) time but the C speed is legendary
	2x2:  0.29s
	3x3:  2.43s
	4x4: 43.12s 
	otherwise is impractical
	(Intel i5 4210M)
	'''
	ciphertext = bytearray(str(ciphertext,"utf-8").replace(" ","").replace("\n","").upper(),"ascii")
	chiSquaredArray = hillcwrapper.frequencyAnalysis(N,ciphertext)
	sortedP = [x for _,x in sorted(zip(chiSquaredArray,range(26**N)))]
	best = [[(p//(26**n))%26 for n in range(N-1,-1,-1)] for p in sortedP[:N]]
	for p in permutations(best):
		if np.linalg.det(p) != 0:
			yield solve(p,N,ciphertext)