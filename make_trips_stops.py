#!/usr/bin/env python
import csv
import os.path

wstops = range(240,253) # 240-252 are Lindenwold to 15th-16th & Locust (Westbound)
estops = range(240,253)
estops.reverse() # Philly to Lindenwold

route_id = 12

# map the csv file names to the days of the week for the service IDs in calendar.txt
service_ids = { 'saturday_sunday': 1, 'monday_wednesday': 2, 'thursday': 3, 'friday': 4 }

# TODO: what's the headsign for the westbound express and train from woodcrest?
directions = {'eastbound':[1,"LINDENWOLD LOCAL",estops],
  'westbound':[0,"PHILADELPHIA LOCAL",wstops]}
special_directions = {'eastbound':[1,"LINDENWOLD SPECIAL"],
  'westbound':[0,"PHILADELPHIA SPECIAL"]}
stop_times_header = ['trip_id','arrival_time','departure_time','stop_id',
  'stop_sequence','pickup_type','drop_off_type']
trips_header = ['route_id','service_id','trip_id','trip_headsign',
                'direction_id', 'shape_id', 'bikes_allowed']
tripId = 4151 # start number for trips (arbitrary)

# read in times when bikes are banned
bike_ban = {}
if os.path.isfile('bike_ban_times.csv'):
  with open('bike_ban_times.csv', 'rb') as bikef:
    rdr = csv.reader(bikef)
    # skip header row
    rdr.next()
    # { 'direction_id': ('service_id', 'start_time', 'end_time') }
    for row in rdr:
      bike_ban[int(row[0])] = (int(row[1]), int(row[2].replace(':','')), int(row[3].replace(':','')))
else:
  print('No bike ban times file found.')

def process_table(direction, service_days):
  global tripId
  inf = open(direction + '_' + service_days + '.csv', 'r')
  print('processing file ' + direction + '_' + service_days + '.csv...')
  for ln in inf:
    flds = ln.split(',')
    times = {}
    maxFld = len(flds)
    x = 0
    this_stop = 0
    isSpecial = False
    startMidnight = False
    bikesAllowed = 1
    directionId = None
    headsign = None
    startFld = flds[0].replace('X', '').replace('W', '').strip().strip('"').strip()
    if startFld.startswith('12') and startFld.endswith('A'):
      startMidnight = True  # use '24' for stop times after midnight
    
    for fld in flds:
      t = fld.strip().strip('"').strip()
      if t.endswith('P') or t.endswith('A'): 
        if t.startswith('X') or t.startswith('W'):
          t = t[1:].strip()
        if t[1] == ':':
          # pad hour with zeroes
          t = '0' + t
        sep = t.find(':')
        hr = t[0:sep]
        mins = t[sep+1:sep+3]
        if t.endswith('A'):
          if hr == '12':
            if startMidnight:
              times[directions[direction][2][this_stop]] = '00:' + mins
            else:
              times[directions[direction][2][this_stop]] = '24:' + mins
          else:
            times[directions[direction][2][this_stop]] = hr + ":" + mins
        else:
          hr = int(hr)
          if hr != 12:
            hr += 12 # military time
          times[directions[direction][2][this_stop]] = str(hr) + ":" + mins      

        wtimes.writerow([tripId,times[directions[direction][2][this_stop]]+':00',
            times[directions[direction][2][this_stop]]+':10',
            directions[direction][2][this_stop], this_stop+1,0,0])
        this_stop += 1
      else:
        # arrow indicating skipped stops (or empty field if multiple skipped)
        isSpecial = True
        this_stop +=1

    # print(isSpecial, len(times), times)
    serviceId = service_ids[service_days]
    if isSpecial:
      directionId = special_directions[direction][0]
      headsign = special_directions[direction][1]
    else:
      directionId = directions[direction][0]
      headsign = directions[direction][1]

    # check if this trip falls within the bike ban times (otherwise bikes are allowed)
    if bike_ban.has_key(directionId):
      ban = bike_ban[directionId]
      if serviceId == ban[0]:
        # on banned direction and service day; check times
        start_stop = 0
        while not times.has_key(directions[direction][2][start_stop]):
          start_stop += 1
        start_str = times[directions[direction][2][start_stop]]
        end_str = times[directions[direction][2][this_stop-1]]
        start_trip = int(start_str.replace(':', ''))
        end_trip = int(end_str.replace(':', ''))
        # if either the start or end time for the trip fall within the ban window, bike ban trip
        if (start_trip >= ban[1] and start_trip <= ban[2]) or (end_trip >= ban[1] and end_trip <= ban[2]):
          print('Trip %s from %s to %s has a bike ban.' % (tripId, start_str, end_str))
          bikesAllowed = 2

    wtrips.writerow((12, serviceId, tripId, headsign, directionId, directionId, bikesAllowed))

    tripId += 1
  inf.close()

outtrips = open('gtfs_files/trips.txt', 'wb')
outstoptimes = open('gtfs_files/stop_times.txt', 'wb')
wtrips = csv.writer(outtrips, quoting=csv.QUOTE_NONNUMERIC)
wtimes = csv.writer(outstoptimes)

# write header rows
wtrips.writerow(trips_header)
wtimes.writerow(stop_times_header)

for d in directions.keys():
  for s in service_ids.keys():
    process_table(d, s)

outtrips.close()
outstoptimes.close()
print('all done!')
