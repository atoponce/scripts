#!/usr/bin/python3

# Get the GPX from Strava. It will have full elevation data for every coordinate
# down to 1 second resolution. On The Go Map has a bunch of holes and MapMyRun
# is missing elevation entirely. Unfortunately, getting the GPX from Strava
# means the altitude data may not be entirely accurate. You might need to get
# the GPX from another athlete.

import math
import gpxpy
import gpxpy.gpx
import matplotlib
import geopy.distance
import matplotlib.pyplot

from pathlib import Path

matplotlib.use("Agg") # Non-interactive. Only writes to files.

def collect_files(n):
    gpx_files = []

    for i in range(n):
        need_file = True

        while need_file:
            f = input(f'Enter GPX path for file {i + 1}: ')

            try:
                gpx_file = open(f, 'r')
            except IOError:
                print(f'  {f} does not exist. Please try again.')
            else:
                gpx_files.append(f)
                need_file = False
    
    return gpx_files

def get_elevations(f):
    dist = 0
    min_elevation = 100000

    gpx_file = open(f, 'r')
    gpx = gpxpy.parse(gpx_file)
    start = gpx.tracks[0].segments[0].points[0]
    prev_coords = (start.latitude, start.longitude)
    length = gpx.length_2d() * 3.28084 / 5280 # meters to miles
    length = math.floor(length * 10) / 10 # accurate to 1/10 mile

    miles = {}
    miles[0.0] = [round(start.elevation * 3.28084, 1)]

    for point in gpx.tracks[0].segments[0].points:
        next_coords = (point.latitude, point.longitude)
        dist += geopy.distance.geodesic(prev_coords, next_coords).mi

        if round(dist, 1) not in miles:
            miles[round(dist, 1)] = [round(point.elevation * 3.28084, 1)]

        prev_coords = next_coords

    for mile, elevation in miles.items():
        if elevation[0] < min_elevation:
            min_elevation = elevation[0]

    for mile, elevation in miles.items():
        miles[mile].append(round(elevation[0] - min_elevation, 1))

    return miles

def build_images(courses):
    pyplot.figure(figsize=(10, 6))

    for course in courses:
        x = []
        y = []

        for mile, elevation in courses[course].items():
            x.append(mile)
            y.append(elevation[1]) # normalized elevation

        pyplot.plot(x, y, label=Path(course).stem)

    pyplot.grid()
    pyplot.xlabel("Miles")
    pyplot.ylabel("Feet above lowest point")
    pyplot.title("Course Elevation Profiles")
    pyplot.legend(loc="best")
    pyplot.savefig('/tmp/course-elevations.png')

def main():
    courses = {}
    count = int(input("How many GPX files are we processing? "))
    gpx_files = collect_files(count)

    for n in range(count):
        course = gpx_files[n]
        courses[course] = get_elevations(course)

    build_images(courses)

if __name__ == "__main__":
    main()
