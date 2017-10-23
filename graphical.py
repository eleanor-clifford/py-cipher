#!/bin/env python3
import core,file,tests
from TWL06 import twl
import tkinter as tk
import matplotlib, numpy, sys, math
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import string

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
			#divisors = Divisors(frame,cipher)
			#test = Test(frame)

		except FileNotFoundError: self.path.set("File Not Found")
	
class BasicAnalysis:
	def __init__(self,master,cipher):
		frame = tk.Frame(master)
		frame.pack(side=tk.LEFT)
		
		self.cipher = cipher
		frequency = core.frequencyList(self.cipher)
		frequency = [100 * (a / sum(frequency)) for a in frequency]
		meanFrequency = [8.17, 1.49, 2.78, 4.25, 12.7, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.02, 2.41, 6.75, 7.51, 1.93, 0.09, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
		
		
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



		



'''
class Test:
	def __init__(self, master):
		frame = tk.Frame(master)
		frame.pack()
		# create a menu
		menu = tk.Menu(master)
		master.config(menu=menu)

		filemenu = tk.Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.callback)
		filemenu.add_command(label="Open...", command=self.callback)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.callback)

		helpmenu = tk.Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About...", command=self.callback)

	def callback(self): print("eh")
'''


start = Start(root)
root.mainloop()

'''
path = input("Enter path of file to read from (cipher.txt): ")
if path == "": path = "cipher.txt"

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

'''