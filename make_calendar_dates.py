#!/usr/bin/env python
import csv

inf = open('use_holidays.txt', 'r')
calf = open('gtfs_files/calendar.txt', 'r')
outf = open('gtfs_files/calendar_dates.txt', 'w')
header = ['service_id','date','exception_type']

# first read calendar file to determine valid date range
rdr = csv.reader(calf)
# skip header row
rdr.next()
svc = rdr.next()
# start and end dates are last two columns in file
start_date = int(svc[len(svc)-2])
end_date = int(svc[len(svc)-1])
calf.close()

print('Scheduling holiday services for dates between %s and %s.' % (start_date, end_date))

writer = csv.writer(outf, quoting=csv.QUOTE_NONE)
reader = csv.reader(inf)
writer.writerow(header)

for ln in reader:
  if len(ln) < 1:
    next
  elif ln[0].startswith('-'):
    next
  else:
    holiday = int(ln[0])
    if holiday >= start_date and holiday <= end_date:
      # remove weekday service
      writer.writerow([1,ln[0],2])
      # add weekend service
      writer.writerow([2,ln[0],1])
    else:
      print('Skipping holiday entry out of range, on %s.' % ln[0])

outf.close()
inf.close()
