import csv

fare_rules_header=['fare_id','origin_id','destination_id']
nj = range(240,249)
phl = range(249,253)

inf = open('fares_to_rev.txt','r')
outf = open('gtfs_files/fare_rules.txt','w')
w = csv.writer(outf)
r = csv.reader(inf)
w.writerow(fare_rules_header)

for ln in r:
    w.writerow(ln)
    w.writerow([ln[0],ln[2],ln[1]])

inf.close()

for x in nj:
    for y in nj:
        if x!=y:
            w.writerow(['nj_nj',x,y])

for x in phl:
    for y in phl:
        if x!=y:
            w.writerow(['phl_phl',x,y])

outf.close()
