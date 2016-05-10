#!/usr/bin/python

import random
rand = random.SystemRandom()
lat = '%.2f'%(rand.randrange(-90,90)*rand.random())
lon = '%.2f'%(rand.randrange(-180,180)*rand.random())
print "http://earth.nullschool.net/#current/wind/surface/level/orthographic={0},{1}/loc={0},{1}".format(lon,lat)
