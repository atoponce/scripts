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
# Performance is ~ 8.5 MiB/s.
# Requires python-pycryptodome: https://www.pycryptodome.org/
#
# Released to the public domain.

import os
import cv2
from Cryptodome.Hash import SHAKE128

webcamfile = '/tmp/webcamfile.fifo'

def frame_diff(frame1, frame2):
    return cv2.absdiff(frame1, frame2)

def max_brightness(frame, value=255):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return frame

def amplify(noise):
    min, max = noise.min(), noise.max()
    amp = 255.0 / (max - min)
    return (noise * amp).astype("uint8")

try:
    os.mkfifo(webcamfile)
except OSError, e:
    print "Cannot create FIFO: {0}".format(e)
else:
    fifo = open(webcamfile, 'w+')

cap = cv2.VideoCapture(0)
framecount = 0
last_frame = None

while True:
    ret, curr_frame = cap.read()
    if not ret:
        break

    if last_frame is not None:
        framecount += 1

        noise = frame_diff(last_frame, curr_frame)
        max_noise = max_brightness(noise)
        amp_noise = amplify(max_noise)

        # Randomness extraction using the SHAKE128 XOF
        # The image size is 640x480. At 2 bytes per pixel, that's 614400 bytes.
        # The XOF hashes all 614400 bytes but only outputs 307200 bytes (1/2).
        # This will be CPU-intensive. Not recommended for running long-term.
        shake = SHAKE128.new()
        shake.update(bytes(amp_noise))
        digest = shake.read(307200)

        cv2.imshow('webcamlamp', amp_noise)
        if cv2.waitKey(1) & 0xff == 27:
            break

        fifo.write(digest)
        fifo.flush()

    last_frame = curr_frame

fifo.close()
os.remove(webcamfile)
cap.release()
cv2.destroyAllWindows()
