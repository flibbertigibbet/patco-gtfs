#!/usr/bin/env python
import csv
import os.path

wstops = range(240,253) # 240-252 are Lindenwold to 15th-16th & Locust (Westbound)
estops = range(240,253)
estops.reverse() # Philly to Lindenwold

route_id = 12

# map the csv file names to the days of the week for the service IDs in calendar.txt
service_ids = { 'monday_wednesday': 1, 'thursday': 2, 'friday': 3, 'saturday_sunday': 4, 'sept4': 5, 'sept7': 6 }

# TODO: what's the headsign for the westbound express and train from woodcrest?
DIR = {'eastbound':[1, "LINDENWOLD LOCAL", estops],
       'westbound': [0, "PHILADELPHIA LOCAL", wstops]
      }
SPECIAL_DIR = {'eastbound': [1, "LINDENWOLD SPECIAL"],
               'westbound':[0, "PHILADELPHIA SPECIAL"]}

STOP_HEADER = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 
               'stop_sequence', 'pickup_type', 'drop_off_type']

TRIP_HEADER = ['route_id', 'service_id', 'trip_id', 'trip_headsign', 
                'direction_id', 'shape_id', 'bikes_allowed']

trip_id = 4151 # start number for trips (arbitrary)

# read in times when bikes are banned
bike_ban = {}
if os.path.isfile('bike_ban_times.csv'):
    with open('bike_ban_times.csv', 'rb') as bikef:
        rdr = csv.reader(bikef)
        # skip header row
        rdr.next()
        # { 'direction_id': ('service_id', 'start_time', 'end_time') }
        for row in rdr:
            bike_ban[int(row[0])] = (int(row[1]), int(row[2].replace(':', '')), int(row[3].replace(':', '')))
else:
    print('No bike ban times file found.')

def process_table(direction, service_days):
    global trip_id
    inf = open(direction + '_' + service_days + '.csv', 'r')
    print('processing file ' + direction + '_' + service_days + '.csv...')
    for ln in inf:
        flds = ln.split(',')
        times = {}
        this_stop = 0
        is_special = False
        start_midnight = False
        bikes_allowed = 1
        direction_id = None
        headsign = None
        start_fld = flds[0].replace('X', '').replace('W', '').strip().strip('"').strip()
        if start_fld.startswith('12') and start_fld.endswith('A'):
            start_midnight = True  # use '24' for stop times after midnight

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
                        if start_midnight:
                            times[DIR[direction][2][this_stop]] = '00:' + mins
                        else:
                            times[DIR[direction][2][this_stop]] = '24:' + mins
                    else:
                        times[DIR[direction][2][this_stop]] = hr + ":" + mins
                else:
                    hr = int(hr)
                    if hr != 12:
                        hr += 12 # military time
                    times[DIR[direction][2][this_stop]] = str(hr) + ":" + mins

                WRITE_TIMES.writerow([trip_id, times[DIR[direction][2][this_stop]]+':00',
                                     times[DIR[direction][2][this_stop]]+':10',
                                     DIR[direction][2][this_stop], this_stop + 1, 0, 0])
                this_stop += 1
            else:
                # arrow indicating skipped stops (or empty field if multiple skipped)
                is_special = True
                this_stop += 1

        # print(is_special, len(times), times)
        service_id = service_ids[service_days]
        if is_special:
            direction_id = SPECIAL_DIR[direction][0]
            headsign = SPECIAL_DIR[direction][1]
        else:
            direction_id = DIR[direction][0]
            headsign = DIR[direction][1]

        # check if this trip falls within the bike ban times (otherwise bikes are allowed)
        if bike_ban.has_key(direction_id):
            ban = bike_ban[direction_id]
            if service_id == ban[0]:
                # on banned direction and service day; check times
                start_stop = 0
                while not times.has_key(DIR[direction][2][start_stop]):
                    start_stop += 1
                start_str = times[DIR[direction][2][start_stop]]
                end_str = times[DIR[direction][2][this_stop-1]]
                start_trip = int(start_str.replace(':', ''))
                end_trip = int(end_str.replace(':', ''))
                # if either the start or end time for the trip fall within the ban window, bike ban trip
                if (start_trip >= ban[1] and start_trip <= ban[2]) or (end_trip >= ban[1] and end_trip <= ban[2]):
                    print('Trip %s from %s to %s has a bike ban.' % (trip_id, start_str, end_str))
                    bikes_allowed = 2

        WRITE_TRIPS.writerow((12, service_id, trip_id, headsign, direction_id, direction_id, bikes_allowed))

        trip_id += 1
    inf.close()

OUT_TRIPS = open('gtfs_files/trips.txt', 'wb')
OUT_STOP_TIMES = open('gtfs_files/stop_times.txt', 'wb')
WRITE_TRIPS = csv.writer(OUT_TRIPS, quoting=csv.QUOTE_NONNUMERIC)
WRITE_TIMES = csv.writer(OUT_STOP_TIMES)

# write header rows
WRITE_TRIPS.writerow(TRIP_HEADER)
WRITE_TIMES.writerow(STOP_HEADER)

for d in DIR.keys():
    for s in service_ids.keys():
        process_table(d, s)

OUT_TRIPS.close()
OUT_STOP_TIMES.close()
print('all done!')
