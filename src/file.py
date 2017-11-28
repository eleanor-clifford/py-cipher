'''
'''
def openAsAscii(path):
	if path == "": path = "cipher.txt"	
	file = open(path,"rb")
	data = file.read()
	udata = data.decode("utf-8")
	bytearray = udata.encode("ascii",errors="ignore")
	bytearray = bytearray.replace(bytes([ord("\n")]),bytes([ord(" ")]))
	return bytearray