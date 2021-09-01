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

import re
import random

def fractionated_morse(text, key):
    code = ''
    mapping = ['···', '··−', '··×', '·−·', '·−−', '·−×', '·×·', '·×−', '·××',
               '−··', '−·−', '−·×', '−−·', '−−−', '−−×', '−×·', '−×−', '−××',
               '×··', '×·−', '×·×', '×−·', '×−−', '×−×', '××·', '××−']

    morse_code = { # Letters
                  'A': '·−×',   'B': '−···×', 'C': '−·−·×', 'D': '−··×',  'E': '·×',    'F': '··−·×',
                  'G': '−−·×',  'H': '····×', 'I': '··×',   'J': '·−−−×', 'K': '−·−×',  'L': '·−··×',
                  'M': '−−×',   'N': '−·×',   'O': '−−−×',  'P': '·−−·×', 'Q': '−−·−×', 'R': '·−·×',
                  'S': '···×',  'T': '−×',    'U': '··−×',  'V': '···−×', 'W': '·−−×',  'X': '−··−×',
                  'Y': '−·−−×', 'Z': '−−··×',
                  # Numbers
                  '1': '·−−−−×', '2': '··−−−×', '3': '···−−×', '4': '····−×', '5': '·····×',
                  '6': '−····×', '7': '−−···×', '8': '−−−··×', '9': '−−−−·×', '0': '−−−−−×',
                  # Punctuation
                  '.': '·−·−·−×', ',': '−−··−−×',  '?': '··−−··×', "'": '·−−−−·×', '!': '−·−·−−×',
                  '/': '−··−·×',  '(': '−·−−·×',   ')': '−·−−·−×', '&': '·−···×',  ':': '−−−···×',
                  ';': '−·−·−·×', '=': '−···−×',   '+': '·−·−·×',  '-': '−····−×', '_': '··−−·−×',
                  '"': '·−··−·×', '$': '···−··−×', '@': '·−−·−·×',
                  # Non-Latin (without the Ch digraph)
                  'À': '·−−·−×', 'Ä': '·−·−×',  'Å': '·−−·−×',   'Ą': '·−·−×',   'Æ': '·−·−×',
                  'Ć': '−·−··×', 'Ĉ': '−·−··×', 'Ç': '−·−··×',   'Đ': '··−··×',  'Ð': '··−−·×',
                  'É': '··−··×', 'È': '·−··−×', 'Ę': '··−··×',   'Ĝ': '−−·−·×',  'Ĥ': '−−−−×',
                  'Ĵ': '·−−−·×', 'Ł': '·−··−×', 'Ń': '−−·−−×',   'Ñ': '−−·−−×',  'Ó': '−−−·×',
                  'Ö': '−−−·×',  'Ø': '−−−·×',  'Ś': '···−···×', 'Ŝ': '···−·×',  'Š': '−−−−×',
                  'Þ': '·−−··×', 'Ü': '··−−×',  'Ŭ': '··−−×',    'Ź': '−−··−·×', 'Ż': '−−··−×',
                  # Space (last word character is already '×')
                  ' ': '×',
                 }

    text = text.upper()
    key = key.upper()

    # Whitelisted characters
    text = re.sub('[^ A-Z0-9.,?\'!/()&:;=+\-_"$@ÀÄÅĄÆĆĈÇĐÐÉÈĘĜĤĴŁŃÑÓÖØŚŜŠÞÜŬŹŻ]', '', text)

    for m in morse_code:
        text = text.replace(m, morse_code[m])

    # Remove trailing '×'
    text = text.rstrip(text[-1])

    if len(text) % 3 == 1:
        text += '××'
    elif len(text) % 3 == 2:
        text += '×'

    for i in range(0, len(text), 3):
        code += key[mapping.index(text[i:i + 3])]

    return code

def columnar_transposition(text, key):
    block = ''
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    indx = [key.index(char) for char in alph]

    padding = 26 - (len(text) % 26)
    text += alph[padding - 1] * padding

    for i in range(len(key)):
        block += text[indx[i]::len(key)]

    return block

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

plaintext = (
            'There are two main things that can affect the result of FtHoF, the current season '
            'and the golden cookie sound selector. If the season is Valentines or Easter the '
            'random seed will be increased once, if the golden cookie sound selector is on then '
            'the seed will also be increased. This means there are 3 possible results for each '
            'cast of FtHoF depending on the selected season or whether the golden cookie chime is '
            'on or both. Continuing to switch between seasons or turn the chime on and off will '
            'not affecting the results, they only affect the result at the time the spell is cast. '
            )

fractionated = fractionated_morse(plaintext, key1)
transposed = columnar_transposition(fractionated, key2)
encrypted = chaocipher(transposed, key1, key2)

print('key1: ', key1)
print('key2: ', key2)
print()
print('Plaintext:\n', plaintext)
print()
print('Fractionated Morse (key1):\n', fractionated)
print()
print('Columnar transposition (key2):\n', transposed)
print()
print('Ciphertext (key1 & key2):\n', encrypted)
