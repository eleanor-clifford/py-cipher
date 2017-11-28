#!/bin/env python3
from src import core,file,tests,vigenere; from src.TWL06 import twl
import tkinter as tk
import string
import matplotlib, numpy, sys, math; matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
root = tk.Tk()

class Start:
	def __init__(self,master):
		frame = tk.Frame(master)
		frame.pack()

		self.prompt = tk.Label(frame,text="Path of cipher")
		self.prompt.pack()

		self.path = tk.StringVar()
		self.path.set("cipher.txt")
		self.pathEntry = tk.Entry(frame, textvariable=self.path)
		self.pathEntry.pack()

		self.go = tk.Button(frame,text="GO", command=self.Analyse)
		self.go.pack(side=tk.LEFT)

		self.train = tk.Button(frame,text="TRAIN", command=self.Train)
		self.train.pack(side=tk.LEFT)
	def Train(self):
		translator = str.maketrans('', '', string.punctuation)
		text = str(file.openAsAscii(self.path.get()),"utf-8").replace("\n"," ").translate(translator).split()
		for word in text:
			if not twl.check(word.lower()): twl.add(word.lower())
	def Analyse(self):
		try:
			cipher = file.openAsAscii(self.path.get())
			
			frame = tk.Frame()
			frame.pack(side=tk.LEFT)
			basic = BasicAnalysis(root,cipher)
			tests = Tests(root,cipher)
			if not IGNORE_POLY:
				poly = PolyAnalysis(root,cipher)
				divisors = Divisors(frame,cipher)
				test = Test(frame)

		except FileNotFoundError: self.path.set("File Not Found")
	
class BasicAnalysis:
	def __init__(self,master,cipher):
		frame = tk.Frame(master)
		frame.pack(side=tk.LEFT)
		
		#a = open("splits.txt").read().split("\n")
		#print("\n".join(a))
		#self.cipher = bytearray(a[3],"ascii")
		self.cipher = cipher
		frequency = core.frequencyList(self.cipher)
		#print(max(frequency))
		frequency = [100 * (a / sum(frequency)) for a in frequency]
		meanFrequency = [8.17, 1.49, 2.78, 4.25, 12.7, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.02, 2.41, 6.75, 7.51, 1.93, 0.09, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
		#meanFrequency = core.frequencyList(bytearray(a[1],"ascii"))
		
		f = Figure(figsize=(5,4), dpi=100)
		ax = f.add_subplot(111)
		ind = numpy.arange(26)
		width = .35

		cipherRects = ax.bar(ind, frequency, width, color="r")
		meanRects = ax.bar(ind + width, meanFrequency, width, color="g")
		ax.set_title("Letter Frequency")
		ax.set_ylabel('Percentage of text')
		ax.set_xticks(ind)
		ax.set_xticklabels([a for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
		ax.legend((cipherRects[0], meanRects[0]), ('Ciphertext', 'English Mean'))

		canvas = FigureCanvasTkAgg(f, master=frame)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		stdDevCipher = math.sqrt(sum([a**2 for a in frequency])/26 - (sum(frequency)/26)**2)
		stdDevMean = math.sqrt(sum([a**2 for a in meanFrequency])/26 - (sum(meanFrequency)/26)**2)
		
		self.stdDev = tk.Label(frame,text="Standard Deviation - Ciphertext {ciphertext:.{digits}f}, English Mean {mean:.{digits}f}"
			.format(ciphertext=stdDevCipher, mean=stdDevMean, digits=2))
		self.stdDev.pack()

		translator = str.maketrans('', '', string.punctuation)
		length = len(str(cipher,"utf-8").replace("\t","").replace("\n","").replace(" ","").translate(translator))
		divisors = [a for a in range(1,length+1) if length % a == 0]
		divLabel = tk.Label(frame,text="Divisors: {0}".format(divisors))
		divLabel.pack()
		'''
		a,b = vigenere.kasiski(self.cipher)
		ksLabel = tk.Label(frame,text="Kasiski: {0} from {1} matches".format(a,b))
		ksLabel.pack()
		'''
class PolyAnalysis:
	def __init__(self,master,cipher):
		self.frame = tk.Frame(master)
		self.frame.pack(side=tk.LEFT)
		self.cipher = cipher
		
		self.info()
		self.graph()
	def graph(self):	
		f = Figure(figsize=(5,4), dpi=100)
		ax = f.add_subplot(111)
		ind = numpy.arange(26)
		width = .35
		with open("splits.txt") as file:
			split_ = file.readline()[:-1]
			split_ = file.readline()[:-1]
			split_ = file.readline()[:-1]
			print(len(split_))
			split_ = file.readline()[:-1]			
			
			split0 = file.readline()[:-1]
			split1 = file.readline()[:-1]
		
		frequency0 = core.frequencyList(bytearray(split0,"ascii"))
		frequency1 = core.frequencyList(bytearray(split1,"ascii"))
		frequency0 = [100 * (a / sum(frequency0)) for a in frequency0]
		frequency1 = [100 * (a / sum(frequency1)) for a in frequency1]		
		#print(frequency0)

		rects0 = ax.bar(ind, frequency0, width, color="r")
		rects1 = ax.bar(ind + width, frequency1, width, color="g")
		ax.set_title("Letter Frequency")
		ax.set_ylabel('Percentage of text')
		ax.set_xticks(ind)
		ax.set_xticklabels([a for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
		ax.legend((rects0[0], rects0[0]), ('Split 0', 'Split 1'))

		canvas = FigureCanvasTkAgg(f, master=self.frame)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		

	def info(self):
		with open("splits.txt","w"): pass
		frame = tk.Frame(self.frame)
		frame.pack()
		infoText = tk.Text(frame)
		infoText.pack()

		keylength,matches = vigenere.kasiskiNoSpace(self.cipher)
		formatter = "\tLength {:d}: {:s}\n"*len(keylength)
		vanillaVigenereKeys = [[k,vigenere.freqAnalysis(length=k,ciphertext=self.cipher)] for k in keylength]
		infoText.insert(tk.INSERT,
				"Basic Vigenere Key (from {:d} matches)\n".format(matches)
				+formatter.format(*sum(vanillaVigenereKeys,[])))
		infoText.insert(tk.INSERT,"\n")
		vigenereAlignKeys = [[k,vigenere.align(splits=splits.split("\n"))] 
				for k,splits in zip(keylength,open("splits.txt").read().split("\n\n"))]
		infoText.insert(tk.INSERT,
				"Vigenere Alignment Key (from {:d} matches)\n".format(matches)
				+formatter.format(*sum(vigenereAlignKeys,[])))

		infoText.config(state=tk.DISABLED)

class Tests:
	def __init__(self, master, cipher):
		self.frame = tk.Frame(master)
		self.frame.pack(side=tk.LEFT)
		
		self.cipher = cipher

		self.affine = tk.Button(self.frame,text="Affine Test", command=self.Affine)
		self.affine.pack()
		affineFrame = tk.Frame(self.frame)
		affineFrame.pack()
		self.function = tk.StringVar()
		self.functionLabel = tk.Label(affineFrame, textvariable=self.function)

		self.mas = tk.Button(self.frame,text="MAS Test", command=self.SetupMAS)
		self.mas.pack()

		self.alphabetText = tk.Text(self.frame, height=2, width=52)
		
		self.vigenere = tk.Button(self.frame,text="Vigenere", command=self.SetupVigenere)
		self.vigenere.pack()

		self.hill = tk.Button(self.frame,text="Hill", command = self.Hill)
		self.hill.pack()
	def Affine(self):
		cipherStart = bytearray("".join([str(a,"utf-8") for a in self.cipher.split()[:10]]),"ascii")
		success,a,b = tests.affine(cipherStart)
		if success:
			self.function.set("D(x): x -> {0}(x - {1}) mod 26".format(a,b))
			with open("output.txt","w") as f:
				print(str(core.shiftLinear(lambda x, a, b: a*(x-b), self.cipher, a, b),"utf-8"),file=f)
			with open("output.txt","r") as output:
				self.outputText = tk.Text(tk.Toplevel())
				text="".join(output.readlines())
				self.outputText.insert(tk.INSERT, text)
			self.outputText.pack()
			self.functionLabel.pack()
				
	def SetupMAS(self):
		frame = tk.Frame(self.frame)
		frame.pack()
		label = tk.Label(frame,text="Monoalphabetic Substitution")
		label.pack()
		subFrame = tk.Frame(frame)
		subFrame.pack()
		prompt = tk.Label(subFrame,text="Cribs: ")
		prompt.pack(side=tk.LEFT)
		self.cribs = tk.StringVar()
		self.cribs.set("the and")
		cribsEntry = tk.Entry(subFrame, textvariable=self.cribs)
		cribsEntry.pack(side=tk.LEFT)
		
		self.mas.config(command=self.MAS)
	def MAS(self):
		self.tupleArray, self.alphabet = tests.mas(self.cipher,self.cribs.get().split())
		with open("alphabet.txt","r") as a: self.alphabetText.insert(tk.INSERT,"".join(a.readlines()))
		self.alphabetText.pack()

		self.outputText = tk.Text(tk.Toplevel())
		with open("output.txt","r") as out:
			self.outputText.insert(tk.END,"".join(out.readlines()))
		self.outputText.pack()
		subFrame = tk.Frame(self.frame)
		subFrame.pack()
		self.fill = tk.Button(subFrame,text="FILL",command=lambda: self.FinishMAS("",True))
		self.mod = tk.Button(subFrame,text="MODIFY",command=lambda: self.FinishMAS(self.alphabetText.get("1.0",tk.END),False))
		self.fill.pack(side=tk.LEFT)
		self.mod.pack(side=tk.LEFT)


	def FinishMAS(self, alphabetText, fill):
		tupleArray=self.tupleArray
		alphabet=self.alphabet
		if alphabetText == "": tests.FinishMAS("","",True,tupleArray,alphabet)
		else: 
			split = alphabetText.split("\n")
			zipped = [(a,b) for a,b in zip(split[0],split[1]) if (a != " " and b != " ")]
			unzipped = [a for a in zip(*zipped)]
			plain,cipher = "".join(unzipped[0]),"".join(unzipped[1]) 
			tests.FinishMAS(plain,cipher,False,tupleArray,alphabet)
		with open("alphabet.txt","w") as a: alphabet.show(file=a)
		self.alphabetText.delete("1.0",tk.END)
		with open("alphabet.txt","r") as a: self.alphabetText.insert(tk.END,"".join(a.readlines()))
		self.outputText.delete("1.0",tk.END)
		with open("output.txt","r") as out:
			self.outputText.insert(tk.END,"".join(out.readlines()))
		self.outputText.pack()

	def SetupVigenere(self):
		frame = tk.Frame(self.frame)
		frame.pack()
		subFrame = tk.Frame(frame)
		subFrame.pack()
		prompt = tk.Label(subFrame,text="Key: ")
		prompt.pack(side=tk.LEFT)
		self.key = tk.StringVar()
		cribsEntry = tk.Entry(subFrame, textvariable=self.key)
		cribsEntry.pack(side=tk.LEFT)

		self.vigenere.config(command=self.Vigenere)

	def Vigenere(self):
		vigenere.decrypt(keyword=bytearray(self.key.get().upper(),"ascii"),ciphertext=self.cipher)
		self.outputText = tk.Text(tk.Toplevel())
		with open("output.txt","r") as out:
			self.outputText.insert(tk.END,"".join(out.readlines()))
		self.outputText.pack()
	def Hill(self):
		if tests.hill(self.cipher):
			self.outputText = tk.Text(tk.Toplevel())
			with open("output.txt","r") as out:
				self.outputText.insert(tk.END,"".join(out.readlines()))
			self.outputText.pack()
IGNORE_POLY = False
for i in sys.argv:
	if i == "--ignore-poly": IGNORE_POLY = True
start = Start(root)
root.mainloop()