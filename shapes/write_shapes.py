#!/usr/bin/env python

# Generate shapes.txt from csv of distances traveled between each point
# on the LineString.

import csv

inf = open('shape_distances.csv', 'rb')
rdr = csv.reader(inf)
outf = open('../gtfs_files/shapes.txt', 'wb')
wtr = csv.writer(outf)

rdr.next()
dist = []
for row in rdr:
    # point 290 is Lindenwold station
    if int(row[0]) < 291:
        dist.append(row)

inf.close()

# first point, which is station at 15th and Locust
first_pt = (39.948484, -75.1669988)

wtr.writerow(('shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence', 'shape_dist_traveled'))

# shape 1 is 15th & Locust to Lindenwold; shape 0 is reverse
# (matches direction_id in trips.txt)

# add shape 1
dist_so_far = 0.0
wtr.writerow((1, first_pt[0], first_pt[1], 1, dist_so_far))
for row in dist:
    dist_so_far += float(row[3])
    wtr.writerow((1, row[1], row[2], row[0], dist_so_far))

# add shape 2
dist.reverse()
dist_so_far = 0.0
wtr.writerow((0, dist[0][1], dist[0][2], 1, dist_so_far))
ct = 2
last_dist = float(dist[0][3])
for row in dist[1:]:
    dist_so_far += last_dist
    wtr.writerow((0, row[1], row[2], ct, dist_so_far))
    last_dist = float(row[3])
    ct += 1

dist_so_far += last_dist
wtr.writerow((0, first_pt[0], first_pt[1], 290, dist_so_far))

outf.close()
