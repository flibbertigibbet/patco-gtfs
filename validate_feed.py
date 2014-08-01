#!/usr/bin/python

import subprocess, sys

feed_file = 'gtfs_files/patco.zip'

print("Validating GTFS...")

p = subprocess.Popen(['feedvalidator.py', '--output=CONSOLE', 
                      '-m', '-n', feed_file], stdout=subprocess.PIPE)
out = p.communicate()
res = out[0].split('\n')
for ln in res:
    print(ln)  
# find output line with count of errors/warnings
errct = res[-2:-1][0]
if errct.find('error') > -1:
    print("Feed validator found errors in " + feed_file + ":  " + errct + ".")
    sys.exit(1)
elif out[0].find('this feed is in the future,') > -1:
    print("Warning!  Feed validator found GTFS not in service until future.")
    sys.exit(0)  # still return success
else:
    if errct.find('successfully') > -1:
        print("Feed looks great:  " + errct + ".")
    else:
        # have warnings
        print("Feed " + feed_file + " looks ok:  " + errct[7:] + ".")
    sys.exit(0)
