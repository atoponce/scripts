#!/usr/bin/env python

# A simple script to show the cryptography elements of:
#   * Fractionation
#   * Transposition
#   * Substitution
#
# On their own, they may not be very secure. But whan combined together, greatly increase the
# difficulty in cracking the code.
#
# It should be assumed that the resulting ciphertext is still insecure.
#
# Public domain

import random

def fractionated_morse(text, key):
    code = ''
    mapping = ['...', '..-', '..x', '.-.', '.--', '.-x', '.x.', '.x-', '.xx',
               '-..', '-.-', '-.x', '--.', '---', '--x', '-x.', '-x-', '-xx',
               'x..', 'x.-', 'x.x', 'x-.', 'x--', 'x-x', 'xx.', 'xx-']

    morse_code = {'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',    'F': '..-.',
                  'G': '--.',  'H': '....', 'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
                  'M': '--',   'N': '-.',   'O': '---',  'P': '.--.', 'Q': '--.-', 'R': '.-.',
                  'S': '...',  'T': '-',    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
                  'Y': '-.--', 'Z': '--..'}

    text = text.upper()
    key = key.upper()

    for k in morse_code:
        text = text.replace(k, morse_code[k] + 'x')

    text = text.replace(' ', 'x')
    text = text.rstrip(text[-1])

    if len(text) % 3 == 1:
        text += 'xx'
    elif len(text) % 3 == 2:
        text += 'x'

    for i in range(0, len(text), 3):
        code += key[mapping.index(text[i:i + 3])]

    return code

def columnar_transposition(text, key):
    block = []

    text = text.upper()
    key = key.upper()

    if len(text) / 26 >  int(len(text) / 26):
        rows = int(len(text) / 26) + 1
    else:
        rows = int(len(text) / 26)

    # 1. Build the columns and rows
    for i in range(rows):
        block.append(text[26 * i: 26 * i + 26])

    # add padding
    padding = 26 - len(block[-1])
    char = chr(65 + padding - 1)

    while len(block[-1]) < 26:
        block[-1] += char

    # 2. Sort the columns
    for n in range(65, 91):
        column = key.index(chr(n))

        for row in range(len(block)):
            tmp = list(block[row])
            tmp[n - 65], tmp[column] = tmp[column], tmp[n - 65]
            block[row] = ''.join(tmp)

            tmp = list(key)
            tmp[n - 65], tmp[column] = tmp[column], tmp[n - 65]
            key = ''.join(tmp)

    # 3. Read the columns
    text = ''
    for n in range(26):
        for idx, row in enumerate(block):
            text += block[idx][n]

    return text

def chaocipher(text, left, right):
    ciphertext = ''
    text = text.upper()
    left = list(left.upper())
    right = list(right.upper())

    for n in range(len(text)):
        char = text[n]

        idx = right.index(char)
        ciphertext += left[idx]

        # Permute left
        for i in range(idx):
            left.append(left.pop(0))    # rotate idx to zenith
        char = left.pop(1)              # extract zenith + 1
        left.insert(13, char)           # insert at nadir

        # Permute right
        for i in range(idx + 1):
            right.append(right.pop(0))  # rotate idx to zenith - 1
        char = right.pop(2)             # extract zenith + 2
        right.insert(13, char)          # insert at nadir

    return ciphertext

rand = random.SystemRandom()
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

rand.shuffle(alphabet)
key1 = ''.join(alphabet)

rand.shuffle(alphabet)
key2 = ''.join(alphabet)

# The plaintext of the Zodiac 340 cipher. If he had deployed something like this script, would it
# have been solved sooner, or still remain unbroken?
plaintext = ('I HOPE YOU ARE HAVING LOTS OF FUN IN TRYING TO CATCH ME THAT WASNT ME ON THE TV SHOW '
             'WHICH BRINGS UP A POINT ABOUT ME I AM NOT AFRAID OF THE GAS CHAMBER BECAUSE IT WILL '
             'SEND ME TO PARADICE ALL THE SOONER BECAUSE I NOW HAVE ENOUGH SLAVES TO WORK FOR ME '
             'WHERE EVERYONE ELSE HAS NOTHING WHEN THEY REACH PARADICE SO THEY ARE AFRAID OF DEATH '
             'I AM NOT AFRAID BECAUSE I KNOW THAT MY NEW LIFE IS LIFE WILL BE AN EASY ONE IN '
             'PARADICE DEATH')

fractionated = fractionated_morse(plaintext, key1)
transposed = columnar_transposition(fractionated, key2)
encrypted = chaocipher(transposed, key1, key2)

print('Plaintext: ', plaintext)
print()
print('key1: ', key1)
print('key2: ', key2)
print()
print('Ciphertext: ', encrypted)
