

| :exclamation:  | This is a mirror of [https://git.sr.ht/~ecc/py-cipher](https://git.sr.ht/~ecc/py-cipher). Please refrain from using GitHub's issue and PR system.  |
|----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|


# py-cipher
A few common tools for classical cipher cracking, implemented in Python 3 and C. Uses fogleman's TWL06

### Prerequisites

- Python 3 interpeter
- C compiler

### Setting up

- Compile the C library (example with gcc):
```bash
$ gcc -Ofast -fPIC -shared -o src/libhill.so src/hillmodule.c
```

- Run the graphical interface:
```bash
$ python3 main.py
```

### Supported ciphers

- Affine ciphers (which includes Caesar shifts and Atbash ciphers)
- All monoalphabetic ciphers as long as the word spacing is consistent with the plaintext
- Vigenere ciphers - including vigenere on top of a monoalphabetic cipher
- Hill ciphers with matrix size up to 4x4