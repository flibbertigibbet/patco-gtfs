patco-gtfs
==========

Build [GTFS](https://developers.google.com/transit/gtfs/) files using data extracted from [PATCO's PDF schedule](http://www.ridepatco.org/schedules/schedules.asp).

I've been uploading the results of the process to the GTFS Data Exchange:
<http://www.gtfs-data-exchange.com/agency/patco/>

Build status:
=============
[![](https://travis-ci.org/flibbertigibbet/patco-gtfs.svg)](https://travis-ci.org/flibbertigibbet/patco-gtfs)

To use:
=======
1. Extract data from each table in the schedule PDF into the corresponding direction\_weekday.csv file.

    [Tabula](https://github.com/jazzido/tabula) helps with this, but the result may need some fixing.
    
2. Write the new trips.txt and stop\_times.txt by running make\_trips\_stops.py:
        `python make_trips_stops.py`

3. Modify calendar.txt in the gtfs\_files directory to set the schedule's effective date.

4. Run make\_calendar\_dates.py, first modifying use\_holidays.txt if the holidays in range have changed.
   Be sure to update calendar.txt first, as holidays will be scheduled within the effective date range.

        `python make_calendar_dates.py`
        
5. If the fare prices need updating, modify the fare\_attributes.txt file directly in the gtfs\_files directory.

6. Zip the contents of the gtfs\_files directory, and validate the results with [Google's GTFS validator](https://code.google.com/p/googletransitdatafeed/wiki/FeedValidator).
