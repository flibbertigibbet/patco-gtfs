#!/usr/bin/env python
import csv

inf = open('use_holidays.txt', 'r')
outf = open('gtfs_files/calendar_dates.txt', 'w')
header = ['service_id','date','exception_type']

writer = csv.writer(outf, quoting=csv.QUOTE_NONE)
reader = csv.reader(inf)
writer.writerow(header)

for ln in reader:
  if len(ln) < 1:
    next
  elif ln[0].startswith('-'):
    next
  else:
    # remove weekday service
    writer.writerow([3,ln[0],2])
    # add sunday service
    writer.writerow([1,ln[0],1])

outf.close()
inf.close()
