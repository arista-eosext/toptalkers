#!/usr/bin/env python

import sqlite3
from prettytable import PrettyTable

#Variables
#=========
DB = "/tmp/sampling.db"

query = '''SELECT ip_src as key, ip_dst, vlan, iface_in, SUM(bytes), SUM(packets), ip_proto, src_port, dst_port, tos
from acct_v5
GROUP by ip_src,ip_dst
ORDER BY SUM(bytes) DESC LIMIT 50;
'''


print "Querying for Top Talkers. Please wait..." 
#sqlite handle
conn = sqlite3.connect ( DB )
conn.row_factory = sqlite3.Row
db = conn.cursor()

rows = db.execute(query).fetchall()


#Create Table Headers
table = PrettyTable(['Src IP', 'Dest IP', 'VLAN','In Intf','Total Bytes', 'Total Packets', 'Protocol', 'Src Port', 'Dst Port', 'TOS'])

#Store all entries in a list that way we can parse and make it pretty 
for x in rows:
    table.add_row(x)
conn.commit()
conn.close()

print table
