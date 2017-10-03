# py-cipher
A few common tools for classical cipher cracking, implemented in Python 3. Uses fogleman's TWL06

### Prerequisites

- Python 3

### Common Usage:

##### Test All:
	$ python3 test-all.py
	ZGG ZXP ZGW ZDM
	AFFINE TEST...SUCCESS
	D(x): x -> 25(x-11) mod 26
	The plaintext has been output to output.txt
	Show output? y
	attack at dawn
	
	$ python3 test-all.py
	TSCRC RPFBY WKQAI CMSBQ
	AFFINE TEST...FAILED
	MONOALPHABETIC SUBSTITUTION TEST...FAILED
	KEYWORD TEST...SUCCESS
	The plaintext has been output to output.txt
	Keyword is pliablenesses
	Show output? y
	this is a keyword cipher

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
 - All monoalphabetic ciphers as long as the word spacing is consistent with the plaintext

The program prompts the user several times during the tests for input (i.e.) is this english? 
can you see any more letters to solve? etc. In order to keep stdout relatively tidy, VT100 Control codes are used to
clear some lines after input. However these do not format properly in some environments (basically non unix-like systems.)
On a *nix system, this program is best run on a CLI in order for the control codes to work. 