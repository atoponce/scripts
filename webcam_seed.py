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
# Performance is ~ 2 KiB/s.
# Requires pyblake2: https://pypi.python.org/pypi/pyblake2
#
# Released to the public domain.

import os
import cv2
import pyblake2

cap = cv2.VideoCapture(0)
webcamfile = '/tmp/webcamfile.fifo'
key = os.urandom(64)

try:
    os.mkfifo(webcamfile)
except OSError, e:
    print "Cannot create FIFO: {0}".format(e)
else:
    fifo = open(webcamfile, 'w+')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    b2sum = pyblake2.blake2b(key)
    b2sum.update(frame)
    digest = b2sum.digest()

    fifo.write(digest)
    fifo.flush()

    ### Uncomment if you want to watch the video capture.
    ### The video will freeze after so many fifo writes.
    ### Not sure why. Stream still conitunes

    #cv2.imshow('webcamlamp', frame)
    #k = cv2.waitKey(1) & 0xFF
    #if k == 27:
    #    break

fifo.close()
os.remove(webcamfile)
cap.release()
cv2.destroyAllWindows()
