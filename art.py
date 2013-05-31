#!/usr/bin/env python

# Reimplement the "Drunken Bishop" walk as implemented by OpenSSH. We use a
# larger field size for GnuPG due to SHA1 fingerprint sizes (11x19).
#
# See http://www.dirk-loss.de/sshvis/drunken_bishop.pdf for the algorithm
# and security analysis for OpenSSH.
#
# The field is as defined:
#
#              111111111
#    0123456789012345678
#   +-------------------+x (column)
#  0|                   |
#  1|                   |
#  2|                   |
#  3|                   |
#  4|                   |
#  5|         S         |
#  6|                   |
#  7|                   |
#  8|                   |
#  9|                   |
# 10|                   |
#   +-------------------+
#   y
# (row)
#
# Each position on the board can be represented by its cartesian
# coordinates (x,y). We can assign each positition a numerical value by
# using the equation:
#
#   pos = x + 19y
#
# Each position on the board contains an ASCII character the represents the
# frequency of visits by the bishop. A blank position has not been visited.
# The more the bishop has visited a square, the heavier or more dense the
# ASCII character should be. From dark -> light, the following scale should
# be used:
#
#   "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. "
#
# See the table below (note, this does not necessarily follow OpenSSH):
#
# +-+-+-+-+-+-+-+-+-+-+--+--+--+--+--+--+--+--+--++--+--+
# |0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18||19|20|
# +-+-+-+-+-+-+-+-+-+-+--+--+--+--+--+--+--+--+--++--+--+
# | |.|^|:|l|i|?|{|f|x|X |Z |# |M |W |& |8 |% |@ ||S |E |
# +-+-+-+-+-+-+-+-+-+-+--+--+--+--+--+--+--+--+--++--+--+
#
# 'S' and 'E' are special characters that represent the starting and ending
# location of the bishop respectively. 'S' always starts at coordinates
# (9,5), which is position 103, the center of the board.
#
# Movement is defined by taking the fingerprint, and coverting each
# character to its binary value. For exmaple, the fingerprint:
# 
#   E041 3539 273A 6534 A3E1  9259 22EE E048 8086 060F
#
# has the binary values of:
#
#   1110000001000001 0011010100111001 0010011100101010 0110010100110100
#   1010001111100001 1001001001011001 0010001011101110 1110000001001000
#   1000000010000110 0000011000001111
#
# The movement is found using bit-pairs at a time, left to right, least
# significant bit to most sifginifant bit. So:
#
#               +-----+-----++-----+-----++-----++-----+-----++-----+-----+
# Fingerprint:  |  E  |  0  ||  4  |  1  || ... ||  0  |  6  ||  0  |  F  |
#               +--+--+--+--++--+--+--+--++-----++--+--+--+--++--+--+--+--+
#    Bit-pair:  |11|10|00|00||01|00|00|01|| ... ||00|00|01|10||00|00|11|11|
#               +--+--+--+--++--+--+--+--++-----++--+--+--+--++--+--+--+--+
#        Step:  |4 |3 |2 |1 ||8 |7 |6 |5 || ... ||76|75|74|73||80|79|78|77|
#               +--+--+--+--++--+--+--+--++-----++--+--+--+--++--+--+--+--+
#
# The direction of our drunken bishop follows standard Chess rules for the
# bishop piece, moving only on the diagnal across the beard, which is
# defined as follows:
#
#   +------+-----+
#   | Pair | Dir |
#   +------+-----+       N
#   |  00  | NW  |       ^
#   +------+-----+       |
#   |  01  | NE  |  W <--+--> E
#   +------+-----+       |
#   |  10  | SW  |       v
#   +------+-----+       S
#   |  11  | SE  |
#   +------+-----+
#
# The bishop starts in the center of the board at position 103. So, each
# possible move would place him on the following positions on the board,
# after the first move:
#
#   +------+-----+------+
#   | Pair | Pos | Diff |
#   +------+-----+------+
#   |  00  | 83  | -20  |
#   +------+-----+------+
#   |  01  | 85  | -18  |
#   +------+-----+------+
#   |  10  | 121 | +18  |
#   +------+-----+------+
#   |  11  | 123 | +20  |
#   +------+-----+------+
#
# We must cleanly handle how the bishop behaves when he reaches the edge of
# the board, or a corner. We'll define the types of positions as follows:
#
#   +-------------------+
#   |aTTTTTTTTTTTTTTTTTb|
#   |LMMMMMMMMMMMMMMMMMR|   a = NW corner
#   |LMMMMMMMMMMMMMMMMMR|   b = NE corner
#   |LMMMMMMMMMMMMMMMMMR|   c = SW corner
#   |LMMMMMMMMMMMMMMMMMR|   d = SE corner
#   |LMMMMMMMMMMMMMMMMMR|   T = Top edge
#   |LMMMMMMMMMMMMMMMMMR|   B = Bottom edge
#   |LMMMMMMMMMMMMMMMMMR|   R = Right edge
#   |LMMMMMMMMMMMMMMMMMR|   L = Left edge
#   |LMMMMMMMMMMMMMMMMMR|   M = Middle pos.
#   |cBBBBBBBBBBBBBBBBBd|
#   +-------------------+
#
# When a bishop finds himself in one of these positions, we'll define his
# adjusted movement, if necessary, as follows:
#
#   +-----+------+---------+----------+--------+
#   | Pos | Bits | Heading | Adjusted | Offset |
#   +-----+------+---------+----------+--------+
#   |  a  |  00  |   NW    | no move  |    0   |
#   |     |  01  |   NE    |    E     |   +1   |
#   |     |  10  |   SW    |    S     |   +19  |
#   |     |  11  |   SE    |    SE    |   +20  |
#   +-----+------+---------+----------+--------+
#   |  b  |  00  |   NW    |    W     |   -1   |
#   |     |  01  |   NE    | no move  |    0   |
#   |     |  10  |   SW    |    SW    |   +18  |
#   |     |  11  |   SE    |    S     |   +19  |
#   +-----+------+---------+----------+--------+
#   |  c  |  00  |   NW    |    N     |   -19  |
#   |     |  01  |   NE    |    NE    |   -18  |
#   |     |  10  |   SW    | no move  |    0   |
#   |     |  11  |   SE    |    E     |   +1   |
#   +-----+------+---------+----------+--------+
#   |  d  |  00  |   NW    |    NW    |   -20  |
#   |     |  01  |   NE    |    N     |   -19  |
#   |     |  10  |   SW    |    W     |   -1   |
#   |     |  11  |   SE    | no move  |    0   |
#   +-----+------+---------+----------+--------+
#   |  T  |  00  |   NW    |    W     |   -1   |
#   |     |  01  |   NE    |    E     |   +1   |
#   |     |  10  |   SW    |    SW    |   +18  |
#   |     |  11  |   SE    |    SE    |   +20  |
#   +-----+------+---------+----------+--------+
#   |  B  |  00  |   NW    |    NW    |   -20  |
#   |     |  01  |   NE    |    NE    |   -18  |
#   |     |  10  |   SW    |    W     |   -1   |
#   |     |  11  |   SE    |    E     |   +1   |
#   +-----+------+---------+----------+--------+
#   |  R  |  00  |   NW    |    NW    |   -20  |
#   |     |  01  |   NE    |    N     |   -19  |
#   |     |  10  |   SW    |    SW    |   +18  |
#   |     |  11  |   SE    |    S     |   +19  |
#   +-----+------+---------+----------+--------+
#   |  L  |  00  |   NW    |    N     |   -19  |
#   |     |  01  |   NE    |    NE    |   -18  |
#   |     |  10  |   SW    |    S     |   +19  |
#   |     |  11  |   SE    |    SE    |   +20  |
#   +-----+------+---------+----------+--------+
#   |  M  |  00  |   NW    |    NW    |   -20  |
#   |     |  01  |   NE    |    NE    |   -18  |
#   |     |  10  |   SW    |    SW    |   +18  |
#   |     |  11  |   SE    |    SE    |   +20  |
#   +-----+------+---------+----------+--------+

import gnupg
import sys

file_name = sys.argv[1]
f = open(file_name,'r')

gpg = gnupg.GPG(gnupghome=None)
finger_print = gpg.list_keys(f)[0]['fingerprint']
#finger_print = '93ab'*10

f_bytes, walk, visits = [], [], [0]*208
coins = [' ','.','^',':','l','i','?','{','f','x','X','Z','#','M','W','&','8','%','@']
pos = 104

for c in str(finger_print):
    f_bytes.append(bin(int(c,16))[2:].zfill(4)[:2])
    f_bytes.append(bin(int(c,16))[2:].zfill(4)[2:])

for d in f_bytes:
    if pos == 0:    # NW corner, square 'a'
        if d == '01':
            pos = pos + 1
        elif d == '10':
            pos = pos + 19
        elif d == '11':
            pos = pos + 20
    elif pos == 18:    # NE corner, square 'b'
        if d == '00':
            pos = pos - 1
        elif d == '10':
            pos = pos + 18
        elif d == '11':
            pos = pos + 19
    elif pos == 190:    # SW corner, square 'c'
        if d == '00':
            pos = pos - 19
        elif d == '01':
            pos = pos - 18
        elif d == '11':
            pos = pos - 1
    elif pos == 208:    # SE corner, square 'd'
        if d == '00':
            pos = pos - 20
        elif d == '01':
            pos = pos - 19
        elif d == '10':
            pos = pos - 1
    elif 0 < pos < 18:    # Top edge, square 'T'
        if d == '00':
            pos = pos - 1
        elif d == '01':
            pos = pos + 1
        elif d == '10':
            pos = pos + 18
        else:   # d = '11'
            pos = pos + 20
    elif 190 < pos < 208: # Bottom edge, square 'B'
        if d == '00':
            pos = pos - 20
        elif d == '01':
            pos = pos - 18
        elif d == '10':
            pos = pos - 1
        else:   # d = '11'
            pos = pos + 1
    elif pos in [19, 38, 57, 76, 95, 114, 133, 152, 171]:  # Left edge, square 'L'
        if d == '00':
            pos = pos - 20
        elif d == '01':
            pos = pos - 19
        elif d == '10':
            pos = pos + 18
        else:   # d = '11'
            pos = pos + 19
    elif pos in [37, 56, 75, 94, 113, 132, 151, 170, 189]:  # Right edge, square 'R'
        if d == '00':
            pos = pos - 19
        elif d == '01':
            pos = pos - 18
        elif d == '10':
            pos = pos + 19
        else:   # d = '11'
            pos = pos + 20
    else:   # middle of the board, square 'M'
        if d == '00':
            pos = pos - 20
        elif d == '01':
            pos = pos - 18
        elif d == '10':
            pos = pos + 18
        else:   # d = '11'
            pos = pos + 20
    walk.append(pos)

print walk

# FIXME: there be bugs with different fingerprint values
# FIXME: it's not printing the last row
for s in walk:
    visits[s] = visits[s] + 1
    if visits[s] > 18:
        visits[s] = 18

# FIXME: the ascii art seems to have dots that don't make sense
i,r = 0,''
for v in visits:
    r += coins[v]
    if i % 19 == 18:
        print r
        r = ''
    i = i + 1
