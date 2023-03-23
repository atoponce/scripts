#!/usr/bin/python3

import cv2
import math
import time

def xorshift128plus():
    s0, s1 = 0xFEEDFACECAFEBEEF, math.floor(time.time())

    def _next():
        # Google uses constants 23, 17, & 26 in V8, as per the original xorshift128+ proposal.
        #   - https://github.com/v8/v8/blob/main/src/base/utils/random-number-generator.h#L119-L128
        # Sebastian Vigna updated them to 23, 18, & 5. They are theoretically more robust.
        #   - https://xorshift.di.unimi.it/xorshift128plus.c
        nonlocal s0, s1
        a, b = s0, s1
        a ^= (a << 23) & 0xFFFFFFFFFFFFFFFF
        a ^= a >> 18
        a ^= b
        a ^= b >> 5
        s0, s1 = b, a
        return s0 + s1

    return _next

def main():
    img = cv2.imread('/tmp/entropy.jpeg')
    rows, cols, _ = img.shape
    r = xorshift128plus()
    extracted = ''
    byte_arr = []

    # pre-computed
    von_neumann = {
          0: '',      1: '0',      2: '1',      3: '',      4: '0',     5: '00',     6: '01',     7: '0',     8: '1',     9: '10',    10: '11',    11: '1',    12: '',     13: '0',     14: '1',     15: '',
         16: '0',    17: '00',    18: '01',    19: '0',    20: '00',   21: '000',   22: '001',   23: '00',   24: '01',   25: '010',   26: '011',   27: '01',   28: '0',    29: '00',    30: '01',    31: '0',
         32: '1',    33: '10',    34: '11',    35: '1',    36: '10',   37: '100',   38: '101',   39: '10',   40: '11',   41: '110',   42: '111',   43: '11',   44: '1',    45: '10',    46: '11',    47: '1',
         48: '',     49: '0',     50: '1',     51: '',     52: '0',    53: '00',    54: '01',    55: '0',    56: '1',    57: '10',    58: '11',    59: '1',    60: '',     61: '0',     62: '1',     63: '',
         64: '0',    65: '00',    66: '01',    67: '0',    68: '00',   69: '000',   70: '001',   71: '00',   72: '01',   73: '010',   74: '011',   75: '01',   76: '0',    77: '00',    78: '01',    79: '0',
         80: '00',   81: '000',   82: '001',   83: '00',   84: '000',  85: '0000',  86: '0001',  87: '000',  88: '001',  89: '0010',  90: '0011',  91: '001',  92: '00',   93: '000',   94: '001',   95: '00',
         96: '01',   97: '010',   98: '011',   99: '01',  100: '010', 101: '0100', 102: '0101', 103: '010', 104: '011', 105: '0110', 106: '0111', 107: '011', 108: '01',  109: '010',  110: '011',  111: '01',
        112: '0',   113: '00',   114: '01',   115: '0',   116: '00',  117: '000',  118: '001',  119: '00',  120: '01',  121: '010',  122: '011',  123: '01',  124: '0',   125: '00',   126: '01',   127: '0',
        128: '1',   129: '10',   130: '11',   131: '1',   132: '10',  133: '100',  134: '101',  135: '10',  136: '11',  137: '110',  138: '111',  139: '11',  140: '1',   141: '10',   142: '11',   143: '1',
        144: '10',  145: '100',  146: '101',  147: '10',  148: '100', 149: '1000', 150: '1001', 151: '100', 152: '101', 153: '1010', 154: '1011', 155: '101', 156: '10',  157: '100',  158: '101',  159: '10',
        160: '11',  161: '110',  162: '111',  163: '11',  164: '110', 165: '1100', 166: '1101', 167: '110', 168: '111', 169: '1110', 170: '1111', 171: '111', 172: '11',  173: '110',  174: '111',  175: '11',
        176: '1',   177: '10',   178: '11',   179: '1',   180: '10',  181: '100',  182: '101',  183: '10',  184: '11',  185: '110',  186: '111',  187: '11',  188: '1',   189: '10',   190: '11',   191: '1',
        192: '',    193: '0',    194: '1',    195: '',    196: '0',   197: '00',   198: '01',   199: '0',   200: '1',   201: '10',   202: '11',   203: '1',   204: '',    205: '0',    206: '1',    207: '',
        208: '0',   209: '00',   210: '01',   211: '0',   212: '00',  213: '000',  214: '001',  215: '00',  216: '01',  217: '010',  218: '011',  219: '01',  220: '0',   221: '00',   222: '01',   223: '0',
        224: '1',   225: '10',   226: '11',   227: '1',   228: '10',  229: '100',  230: '101',  231: '10',  232: '11',  233: '110',  234: '111',  235: '11',  236: '1',   237: '10',   238: '11',   239: '1',
        240: '',    241: '0',    242: '1',    243: '',    244: '0',   245: '00',   246: '01',   247: '0',   248: '1',   249: '10',   250: '11',   251: '1',   252: '',    253: '0',    254: '1',    255: ''
    }

    for i in range(rows):
        for j in range(cols):
            # shuffle pixels
            x, y = r() % rows, r() % cols
            img[i, j], img[x, y] = img[x, y], img[i, j]

            # decorrelate bgr across pixels
            x, y = r() % rows, r() % cols
            img[i, j, 0], img[x, y, 0] = img[x, y, 0], img[i, j, 0] # blue

            x, y = r() % rows, r() % cols
            img[i, j, 1], img[x, y, 1] = img[x, y, 1], img[i, j, 1] # green

            x, y = r() % rows, r() % cols
            img[i, j, 2], img[x, y, 2] = img[x, y, 2], img[i, j, 2] # red

            # shuffle the bgr channel
            n = r() % 6
            if n == 0:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 0], img[i, j, 1], img[i, j, 2]
            elif n == 1:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 0], img[i, j, 2], img[i, j, 1]
            elif n == 2:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 1], img[i, j, 0], img[i, j, 2]
            elif n == 3:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 1], img[i, j, 2], img[i, j, 0]
            elif n == 4:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 2], img[i, j, 0], img[i, j, 1]
            else:
                img[i, j, 0], img[i, j, 1], img[i, j, 2] = img[i, j, 2], img[i, j, 1], img[i, j, 0]

            # split up each channel
            x, y = r() % rows, r() % cols

            b1, b2 = img[i, j, 0], img[x, y, 0]
            g1, g2 = img[i, j, 1], img[x, y, 1]
            r1, r2 = img[i, j, 2], img[x, y, 2]

            b1_msb, b1_lsb, b2_msb, b2_lsb = b1 >> 4, b1 & 0xf, b2 >> 4, b2 & 0xf
            g1_msb, g1_lsb, g2_msb, g2_lsb = g1 >> 4, g1 & 0xf, g2 >> 4, g2 & 0xf
            r1_msb, r1_lsb, r2_msb, r2_lsb = r1 >> 4, r1 & 0xf, r2 >> 4, r2 & 0xf

            img[i, j, 0] = b1_msb << 4 | b2_lsb
            img[i, j, 1] = g1_msb << 4 | g2_lsb
            img[i, j, 2] = r1_msb << 4 | r2_lsb

            img[x, y, 0] = b2_msb << 4 | b1_lsb
            img[x, y, 1] = g2_msb << 4 | g1_lsb
            img[x, y, 2] = r2_msb << 4 | r1_lsb

    cv2.imwrite('/tmp/entropy-mixed.jpeg', img)

    # von neumann randomness extraction
    for i in range(rows):
        for j in range(cols):
            extracted += von_neumann[img[i, j, 0]]
            extracted += von_neumann[img[i, j, 1]]
            extracted += von_neumann[img[i, j, 2]]

    # create byte array
    for i in range(0, len(extracted), 8):
        if extracted[i:i + 8] not in ['00000000', '11111111']:
            byte_arr.append(int(extracted[i:i + 8], 2))

    # unbiased random binary data
    with open('/tmp/entropy.bin', 'wb') as f:
        f.write(bytearray(byte_arr))

if __name__ == '__main__':
    main()
