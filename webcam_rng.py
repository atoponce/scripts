#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create true random seeds (near as we can tell) with your webcam.
#
# This script will use your webcam as a source of entropy. There is no need to
# point it at anything. The CCD in the camera is providing enough entropy via
# (sorted in order of most to least entropy):
# 
#   * Dark shot noise- Main source of entropy via thermal fluctuations
#   * Read noise- Sensor design producting electronic RF
#   * Photon shot noise- Noise via the arrival of a photon to the CCD
#   * Radiation noise- Alpha, beta, gamma, x-ray, and proton interaction
# 
# However, if you *really* want to point it at something chaotic, you could
# point the camera at:
#
#   * Rayleigh-Bénard convection
#   * Brownian motion
#   * Plasma globes
#   * Lava lamps
#   * Your ugly mug staring at the computer working
#
# At room temperature with no light, entropy is ~ 0.39 bits per byte
# Requires numpy & python-pycryptodome (https://www.pycryptodome.org/)
#
# Released to the public domain.

import os
import cv2
import numpy
from Cryptodome.Hash import SHAKE128

webcamfile = '/tmp/webcam-rng.fifo'

def max_brightness(frame, value=255):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return frame

try:
    os.mkfifo(webcamfile)
except OSError, e:
    print "Cannot create FIFO: {0}".format(e)
else:
    fifo = open(webcamfile, 'w+')

cap = cv2.VideoCapture(0)
cap.set(3, 640) # set width
cap.set(4, 480) # set height
last_frame = None

while True:
    ret, curr_frame = cap.read()
    if not ret:
        break

    if last_frame is not None:
        frame = curr_frame

        # For visual demonstrations
        # 1. diff two frames
        frame = cv2.absdiff(last_frame, curr_frame)

        # 2. maximize the luminance
        frame = max_brightness(frame)

        # 3. convert to black-and-white
        #frame = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)[1]

        # Randomness extraction using the SHAKE128 XOF
        #
        # The image size is 640x480. My PS3 Eye cam only hase 1 byte per pixel
        # of color depth, which is 307,200 bytes per frame.
        #
        # The raw entropy of each frame, with the camera cooled to 20 degrees
        # Celsius and no light entering the lens, is about 0.11 bits per byte,
        # +/- 0.02 bits per byte. This provides about 33,792-bits of entropy
        # per frame, or 4,224 bytes per frame.
        #
        # The security margin of SHAKE128 is the min(d/2, 128), where "d" is
        # our digest. So by outputting 4096 KB, my collision security margin is
        # between 128-bits to 2,048-bits with SHAKE128. Preimage and 2nd
        # preimage collision resistance will have the full 4,096-bits.
        #
        # The XOF hashes all 307,200 bytes but outputs a conservative 8 KB.
        shake = SHAKE128.new()
        shake.update(bytes(frame))
        digest = shake.read(14976) # 640*480*0.39/8

        cv2.imshow('webcam noise', frame)
        if cv2.waitKey(1) & 0xff == 27:
            break

        fifo.write(digest)
        fifo.flush()

    last_frame = curr_frame

fifo.close()
os.remove(webcamfile)
cap.release()
cv2.destroyAllWindows()
