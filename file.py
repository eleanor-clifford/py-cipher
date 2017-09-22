'''
'''
def openAsAscii(path):
	if path == "": path = "cipher.txt"	
	file = open(path,"rb")
	data = file.read()
	udata = data.decode("utf-8")
	asciiData = udata.encode("ascii",errors="ignore")
	cipher = ""
	for i in asciiData: cipher += chr(i)
	cipher = cipher.replace("\n"," ")
	return cipher