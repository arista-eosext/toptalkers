#!/usr/bin/env python
#
# May 22, 2019 --- Changed VLAN entry if its a routed port.
# 
# 

import sqlite3
from prettytable import PrettyTable

# Variables
# =========
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
    #If its a routed port, then EOS sflow agent sends it as a 32bit number which translate to the 4 octet IP address of the interface.
    # if it's greater than 4095, we need to manipulate the data so it just shows an 'N/A' for this field. 
    if x[2] > 4095:
        # We need to do some hackery here to tweak our field.
        # Can't modify this directly since its a sql object. Nor does this object support copying with list slicing.
        # So we need to copy each field into a temp list.
        modlist=[]
        for eachField in x:
            modlist.append(eachField)
        #Tweak our VLAN field which is offset 2
        modlist[2] = "N/A"
        table.add_row(modlist)
    else:
        table.add_row(x)

conn.commit()
conn.close()

print table
