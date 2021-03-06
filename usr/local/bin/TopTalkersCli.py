#!/usr/bin/env python
# Place this in /usr/lib/python2.7/site-packages/CliPlugin
#
# Extend CLI for TopTalkers Extension.
#
#########################################################################################
# Version 1.0.0  - 11/1/2018 - Jeremy Georges -- jgeorges@arista.com --  Initial Version
# Version 1.4.0  - 12/27/2018 - J.Georges - Added additional exception handling.
#########################################################################################
#
#
import BasicCli
import CliParser
import sqlite3
from prettytable import PrettyTable
import sys
import os

# DB file and location
DB = "/tmp/sampling.db"


#-------------------------------------------------------------------------------
# The "show toptalkers [all]" command 
#-------------------------------------------------------------------------------

def showTopTalkers( mode, whatAll ):
    # Check to make sure the file exists first. If it does not, then display error.
    # Perhaps someone deleted it?
    try:
      os.stat( DB )
    except OSError:
      mode.addError( "Database does not exist. ")
      return

    # We need to do this for the initial please wait message to bypass pagination for our status message
    # Otherwise, we'll never see our Please wait message until the sql query completes.
    msg = "\nQuerying for Top Talkers. Please wait...\n\r"
    terminalName = os.environ.get( "REALTTY" )
    fd = None
    if terminalName:
        try:
            fd = os.open( terminalName, os.O_WRONLY );
        except Exception:
            pass
    if fd:
        os.write( fd, msg )
    elif stdoutIfNoTerminal:
        sys.stdout.write( msg )
        sys.stdout.flush()



    query = '''SELECT ip_src as key, ip_dst, vlan, iface_in, SUM(bytes), SUM(packets), ip_proto, src_port, dst_port, tos
    from acct_v5
    GROUP by ip_src,ip_dst
    ORDER BY SUM(bytes) DESC LIMIT 50;
    '''
    
    queryall = '''SELECT ip_src as key, ip_dst, vlan, iface_in, SUM(bytes), SUM(packets), ip_proto, src_port, dst_port, tos
    from acct_v5
    GROUP by ip_src,ip_dst
    ORDER BY SUM(bytes) DESC;
    '''

    # sqlite handle
    try:
        conn = sqlite3.connect ( DB )
        conn.row_factory = sqlite3.Row
        db = conn.cursor()

        # If whatall is set, then we have 'all' token used and we will not query with a limit.
        if whatAll == None:
            rows = db.execute(query).fetchall()
        else:
            rows = db.execute(queryall).fetchall() 
        if not rows:
            conn.commit()
    except sqlite3.Error as e:
        mode.addError("Database error: %s" % e)
    except Exception as e:
        mode.addError("Exception in query: %s" % e)
    finally:
        if conn:
            conn.close()

    # Create Table Headers
    table = PrettyTable(['Src IP', 'Dest IP', 'VLAN','In Intf','Total Bytes', 'Total Packets', 'Protocol', 'Src Port', 'Dst Port', 'TOS'])

    # Store all entries in a list that way we can parse and make it pretty 
    for x in rows:
        # If its a routed port, then EOS sflow agent sends it as a 32bit number which translate to the 4 octet IP address of the interface.
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

    print table




tokenTopTalkers = CliParser.KeywordRule( 'toptalkers', helpdesc='show toptalkers with local sflow sampling' )
tokenMax = CliParser.KeywordRule(
   'all', helpdesc='Show all toptalkers' )

BasicCli.registerShowCommand( tokenTopTalkers, [ '>>whatAll', tokenMax ], showTopTalkers )

