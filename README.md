# py-cipher
A few common tools for classical cipher cracking, implemented in Python 3. Uses fogleman's TWL06

### Prerequisites

- Python 3

### Common Usage:

##### Test All:
	$ ./test-all.py
	ZGG ZXP ZGW ZDM
	AFFINE TEST...SUCCESS
	attack at dawn
	D(x): x -> 25(x-11) mod 26
	
	$ ./test-all.py
	TSCRC RPFBY WKQAI CMSBQ
	AFFINE TEST...FAILED
	KEYWORD TEST...SUCCESS
	this is a keyword cipher
	Keyword is pliablenesses

### Core module

Functionality:

- Return a list of letter frequency from a given string
- Sort a string with a given linear function into a list of inputs based on letter frequency
- Shift a given string based on a linear function and inputs

Sample Usage:

	>>> from cipher import core
	>>> letterFrequency = core.frequencyList(<encrypted string>)
	>>> core.sortLinear(lambda x, a, b: a(x - b),<encrypted string>,range(1,5),range(26))
	[(<a1>,<b1>),(<a2>,<b2>)...(<a104>,<b104>)]
	>>> core.shiftLinear(lambda x, a, b: a(x - b),<encrypted string>,<a1>,<b1>)
	<possibly decrypted string>

### Dictionary module:

Functionality:

- Recursively check against a scrabble dictionary and list of one letter words and return a Boolean and the decrypted cipher

Sample Usage:

	>>> from cipher import dictionary
	>>> dictionary.filterIgnoreSpace(lambda x, a, b: a*(x - b), <affine cipher>, <list of possible shifts as (a,b)>)
	<decrypted cipher>


### Supported ciphers

 - Affine ciphers (which includes Caesar shifts and Atbash ciphers)
 - Keyword ciphers where the keyword is a member of the TWL06 scrabble dictionary
 - Random keyword ciphers (slow)

As the decryption is tested against a number of obscure words there can sometimes be (especially for short ciphers)
a decryption which is technically correct english, but makes no sense. For this reason, in keyword test, 
the user will sometimes be prompted to ask whether a string is english. After answering the question is cleared from 
stdout (using VT100 control codes) and the program carries on. It is recommended to run the program directly from a 
terminal as the control codes do not format properly otherwise, i.e use

	$ chmod +x test-all.py
	$ ./test-all.py

or

	$ python3 test-all.py

also, this will only format correctly in *nix based systems