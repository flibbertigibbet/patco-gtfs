patco-gtfs
==========

Build [GTFS](https://developers.google.com/transit/gtfs/) files using data extracted from [PATCO's PDF schedule](http://www.ridepatco.org/schedules/schedules.asp).

I've been uploading the results of the process to the GTFS Data Exchange:
<http://www.gtfs-data-exchange.com/agency/patco/>

To use:
=======
1. Extract data from each table in the schedule PDF into the corresponding direction\_weekday.csv file.

    [Tabula](https://github.com/jazzido/tabula) helps with this, but the result may need some fixing.
    
2. Write the new trips.txt and stop\_times.txt by running make\_trips\_stops.py:
        `python make_trips_stops.py`
        
3. If the scheduled holidays need updating, modify use\_holidays.txt and run make\_calendar\_dates.py:
        `python make_calendar_dates.py`
        
4. If the fares need updating, modify the fare\_attributes.txt file directly in the gtfs\_files directory.

5. Modify calendar.txt in the gtfs\_files directory to set the schedule's effective date.

6. Zip the contents of the gtfs\_files directory, and validate the results with [Google's GTFS validator](https://code.google.com/p/googletransitdatafeed/wiki/FeedValidator).
