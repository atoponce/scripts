#!/usr/bin/python

# Create true random seeds (near as we can tell) with your webcam.
#
# This script will use your webcam pointed at a source of entropy, keyed with
# random data from the OS CSPRNG. You could point the camera at:
#
#   * Lava lamps
#   * Plasma globes
#   * Double pendulums
#   * Rayleigh-Benard convection
#   * Brownian motion
#
# Performance is ~ 8.75 MiB/s on my Intel Core 2 Duo T7500
# Requires numpy & python-pycryptodome (https://www.pycryptodome.org/)
#
# Released to the public domain.

import os
import cv2
import numpy
from Cryptodome.Hash import SHAKE128

webcamfile = '/tmp/webcamfile.fifo'

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
    # Simple shuffle: f(x) = ax mod m, where a and m are coprime
    # Linear algorithm- you will still see linear correlations in the frame

    # First shuffle rows
    for row in xrange(480):
        # swap rows
        dest = (401*row) % 480
        source_row = frame[row]
        frame[row] = frame[dest]
        frame[dest] = source_row

        # rotate row
        frame[row] = numpy.roll(frame[row], dest)

    # Now shuffle cols
    for col in xrange(640):
        # swap cols
        dest = (509*col) % 640
        source_col = frame[:,col]
        frame[:,col] = frame[:,dest]
        frame[:,dest] = source_col

        # rotate cols
        frame[:,col] = numpy.roll(frame[:,col], dest)

    return frame

try:
    os.mkfifo(webcamfile)
except OSError, e:
    print "Cannot create FIFO: {0}".format(e)
else:
    fifo = open(webcamfile, 'w+')

cap = cv2.VideoCapture(0)
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

        # 3. convert to grayscale
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 4. decorrelate the frames (reduce bandwidth by 2/3)
        #frame = decorrelate(frame)

        # Randomness extraction using the SHAKE128 XOF
        # The image size is 640x480. At 2 bytes per pixel, that's 614400 bytes.
        # The XOF hashes all 614400 bytes but only outputs 307200 bytes (1/2).
        # This will be CPU-intensive. Not recommended for running long-term.
        shake = SHAKE128.new()
        shake.update(bytes(frame))
        digest = shake.read(307200)

        cv2.imshow('webcamlamp', frame)
        if cv2.waitKey(1) & 0xff == 27:
            break

        fifo.write(digest)
        fifo.flush()

    last_frame = curr_frame

fifo.close()
os.remove(webcamfile)
cap.release()
cv2.destroyAllWindows()
