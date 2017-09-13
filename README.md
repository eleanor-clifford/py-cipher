# py-cipher
A few common tools for classical cipher cracking, implemented in Python 3. Uses fogleman's TWL06

### Prerequisites

- Python 3

### Common Usage:

##### Test All:
    $ ./test-all.py
    ZGGZX PZGWZ DM
    AFFINE TEST...SUCCESS
    attack at dawn
    D(x): x -> 25(x-11) mod 26
    
or:
    
    $ ./test-all.py
    <input>
    AFFINE TEST...FAILED

### Core module

Functionality:

- Return a list of letter frequency from a given string
- Sort a string with a given linear function into a list of inputs based on letter frequency
- Shift a given string based on a linear function and inputs

Sample Usage:

    >>> from cipher import core
    >>> letterFrequency = core.frequencyList(<encrypted string>)
    >>> core.sortLinear(lambda x, a, b: a*x + b,<encrypted string>,range(1,5),range(26))
    [(<a1>,<b1>),(<a2>,<b2>)...(<a104>,<b104>)]
    >>> core.shiftLinear(lambda x, a, b: a*x + b,<encrypted string>,<a1>,<b1>)
    <decrypted string>

### Dictionary module:

Functionality:

- Recursively check against a scrabble dictionary and list of one letter words and return a Boolean and the decrypted cipher

Sample Usage:

    >>> from cipher import dictionary
    >>> dictionary.filterIgnoreSpace(lambda x, a, b: a*x + b, <affine cipher>, <list of possible shifts as (a,b)>)
    <decrypted cipher>

### Supported ciphers

At the moment only Affine ciphers (which includes Caesar shifts and Atbash ciphers) are supported directly, although these tools can be used for much more.
I am looking into adding support for Hill Ciphers

