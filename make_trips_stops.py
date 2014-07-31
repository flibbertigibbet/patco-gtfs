#!/usr/bin/env python
import csv

wstops = range(240,253) # 240-252 are Lindenwold to 15th-16th & Locust (Westbound)
estops = range(240,253)
estops.reverse() # Philly to Lindenwold

route_id = 12

# map the csv file names to the days of the week for the service IDs in calendar.txt
service_ids = {'sunday':1,'saturday':2,'monday_wednesday':3, 'thursday':4, 'friday': 5}

# TODO: what's the headsign for the westbound express and train from woodcrest?
directions = {'eastbound':[1,"LINDENWOLD LOCAL",estops],
  'westbound':[0,"PHILADELPHIA LOCAL",wstops]}
special_directions = {'eastbound':[1,"LINDENWOLD SPECIAL"],
  'westbound':[0,"PHILADELPHIA SPECIAL"]}
stop_times_header = ['trip_id','arrival_time','departure_time','stop_id',
  'stop_sequence','pickup_type','drop_off_type']
trips_header = ['route_id','service_id','trip_id','trip_headsign','direction_id']
tripId = 4151 # start number for trips (arbitrary)

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
    if isSpecial:
      wtrips.writerow([12,service_ids[service_days],tripId,
        special_directions[direction][1], special_directions[direction][0]])
    else:
      wtrips.writerow([12,service_ids[service_days],tripId,
        directions[direction][1], directions[direction][0]])
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
