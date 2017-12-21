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
# Without decorrelation, performance is ~ 8.75 MiB/s on my Intel Core 2 Duo T7500
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

def decorrelate(frame):
    # Simple shuffle: f(x) = (ax+b) mod m, a and m are coprime, b non-zero
    # Linear algorithm- you will still see linear correlations in the frame
    # Possible idea:
    #   - use a nonlinear algorithm like Mix+Permute from the Threefish cipher

    # First shuffle rows
    for row in xrange(480):
        # swap rows
        dest = (211*row + 1) % 480
        source_row = frame[row]
        frame[row] = frame[dest]
        frame[dest] = source_row

        # rotate row
        part = (311*row + 1) % 480
        frame[row] = numpy.roll(frame[row], part)

    # Now shuffle cols
    for col in xrange(640):
        # swap cols
        dest = (409*col + 2) % 640
        source_col = frame[:,col]
        frame[:,col] = frame[:,dest]
        frame[:,dest] = source_col

        # rotate cols
        part = (509*col + 2) % 640
        frame[:,col] = numpy.roll(frame[:,col], part)

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
        # For visual demonstrations
        # 1. diff two frames
        frame = cv2.absdiff(last_frame, curr_frame)

        # 2. maximize the luminance
        frame = max_brightness(frame)

        # 3. convert to black-and-white
        #frame = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)[1]

        # 4. decorrelate the frames (reduces bandwidth by ~ 2/3)
        #frame = decorrelate(frame)

        # Randomness extraction using the SHAKE128 XOF
        # The image size is 640x480. At 2 bytes per pixel, that's 614400 bytes.
        # The XOF hashes all 614400 bytes but only outputs 307200 bytes (1/2).
        # This will be CPU-intensive. Not recommended for running long-term.
        shake = SHAKE128.new()
        shake.update(bytes(frame))
        digest = shake.read(307200)

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
