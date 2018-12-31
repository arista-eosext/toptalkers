#!/usr/bin/env python
# Copyright (c) 2018 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#  - Neither the name of Arista Networks nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
'''
toptalkers agent

The purpose of this extension is to provide on switch top talker support from sflow
samples. Although a centralized sflow collector has some significant benefits,
some remote locations can benefit from having some local samples stored for EOS CLI
troubleshooting.

Add the following configuration snippets to enable.

!
daemon toptalkers
   exec /usr/local/bin/toptalkers
   option MAXFILESIZE value 50000000
   option HOURSOLD value 12
   option CHECKINTERVAL value 1800
   no shutdown
!
--MAXFILESIZE is the max file size in bytes of the database before clean up occurs.
  Default value is 50,000,000 (50MB)
--HOURSOLD is the time in hours to use to clean up old entries. Default is 12 hours
  which means that when MAXFILESIZE is reached, all entries older than HOURSOLD 
  will be deleted and sqlite db will execute VACUUM to reduce file size.
--CHECKINTERVAL is the time in seconds in which toptalker agent will check the file
  size of the database. Default time is 1800 seconds (30min).

'''
#************************************************************************************
# Change log
# ----------
# Version 1.0.0  - 11/01/2018 - Jeremy Georges -- jgeorges@arista.com --  Initial Version
# Version 1.1.0  - 11/02/2018 - J. Georges -- jgeorges@arista.com --  Added agentMgr options
# Version 1.2.0  - 11/05/2018 - J. Georges -- jgeorges@arista.com --  Fixed Bug around db cleanup and defaults
# Version 1.3.0  - 11/07/2018 - J. Georges - jgeorges@arista.com -- Fixed agentOption.status_set typo. Added TOS in show output
# Version 1.4.0  - 12/20/2018 - J. Georges - jgeorges@arista.com -- Changed default timers to be more aggressive. Changed syslog
#                                                                   to LOCAL4 so logs show up in EOS logs.
#                                                                   Added better exception handling.
#
#*************************************************************************************
#
#TODO - future possible changes:
#1. Change our TMPDIR environment variable for our instance to another location with plenty of space
# or maybe we just use PRAGMA temp_store_directory even though its deprecated because EOS is already
# using TMPDIR environment variable? TBD
#2. Change sfacct to log to local4 so we have entries in EOS logs?
#  printf("  -S  \t[ auth | mail | daemon | kern | user | local[0-7] ] \n\tLog to the specified syslog facility\n");
#  Perhaps we leave this this alone since we are pretty verbose with our agent.
#
#
#****************************
#GLOBAL VARIABLES -         *
#****************************
#These are the defaults. We'll let users customize these via agentMgr.agent_option()
#to customize based on customer requirements.
#Set Check Interval in seconds. 1800 is 30min and should be a sufficent default.
CHECKINTERVAL=1800
SQLDBFILE='/tmp/sampling.db'

#If file is in Bytes, then we need to do some cleanup so we don't use up /tmp fs
MAXFILESIZE=50000000

#How old to delete old entries in db if we get a large database. In hours.
#i.e. anything older than x HOURSOLD, will be deleted.
HOURSOLD=12


#****************************
#*     MODULES              *
#****************************
#
import sys
import os
import syslog
import eossdk
import sqlite3
import time

#***************************
#*     FUNCTIONS           *
#***************************
class toptalkersAgent(eossdk.AgentHandler,eossdk.TimeoutHandler):
    def __init__(self, sdk, timeoutMgr):
        self.agentMgr = sdk.get_agent_mgr()
        self.tracer = eossdk.Tracer("toptalkersPythonAgent")
        eossdk.AgentHandler.__init__(self, self.agentMgr)
        #Setup timeout handler
        eossdk.TimeoutHandler.__init__(self, timeoutMgr)
        self.tracer.trace0("Python agent constructed")


    def on_initialized(self):
        self.tracer.trace0("Initialized")
        syslog.syslog("toptalkers Initialized")
        self.agentMgr.status_set("Status:", "Administratively Up")
        #


        #Set up all our options.
        global CHECKINTERVAL
        if self.agentMgr.agent_option("CHECKINTERVAL"):
          self.on_agent_option("CHECKINTERVAL", self.agentMgr.agent_option("CHECKINTERVAL"))
        else:
          #global CHECKINTERVAL
          #We'll just use the default time specified by global variable
          self.agentMgr.status_set("CHECKINTERVAL:", "%s" % CHECKINTERVAL)

        global MAXFILESIZE
        if self.agentMgr.agent_option("MAXFILESIZE"):
          self.on_agent_option("MAXFILESIZE", self.agentMgr.agent_option("MAXFILESIZE"))
        else:
          #We'll just use the default MAXFILESIZE specified by global variable
          self.agentMgr.status_set("MAXFILESIZE:", "%s" % MAXFILESIZE)

        global HOURSOLD
        if self.agentMgr.agent_option("HOURSOLD"):
          self.on_agent_option("HOURSOLD", self.agentMgr.agent_option("HOURSOLD"))
        else:
          #We'll just use the default HOURSOLD specified by global variable
          self.agentMgr.status_set("HOURSOLD:", "%s" % HOURSOLD)

        #IF DB file does not exist, then create DB
        #Call DB Create function.
        if not os.path.exists(SQLDBFILE):
          syslog.syslog("DB File does not exist. Creating.")
          self.create_db()

        ##START SFACCTD
        self.start_sfacctd()

        #Start our handler now.
        self.timeout_time_is(eossdk.now())

    def on_timeout(self):
        #We need our globals here for reference in case they are not set in the configuration
        global MAXFILESIZE
        global HOURSOLD
        global CHECKINTERVAL

        # Set Last Check so we can see it from the EOS CLI.
        self.agentMgr.status_set("Last Check At:", time.asctime( time.localtime(time.time()) ) )


        # If this is first time, then what?
        #CHECK SIZE...because we don't know if someone did a shutdown/no shut and we have an
        #old file here. To be safe, always check in each interation, even if first time through.
        #We don't automatically delete the db on startup, because perhaps user wants to keep historial data
        try:
            DBSIZE=os.path.getsize(SQLDBFILE)
        except Exception as e:
            #If we get an issue, lets log this, e.g. someone deleted the file?.
            syslog.syslog("%s" % e)
            syslog.syslog("db file appears to be unaccessible. Did someone delete %s" % SQLDBFILE)
            #If we get here, we can restart everythingself.
            self.kill_sfacctd()
            #sleep for 5 seconds just to let things stabilize. Before we create new db
            time.sleep(5)
            self.create_db()
            self.start_sfacctd()
            DBSIZE=0


        self.agentMgr.status_set("DB SIZE (Bytes):", "{:,}".format(DBSIZE))

        #generally, we check the /tmp/sampling.db file size. If it exceeds the defined
        #threshold, log and then delete old entries and vacuum.
        if self.agentMgr.agent_option("MAXFILESIZE"):
            MAXSIZE = self.agentMgr.agent_option("MAXFILESIZE")
        else:
            #Else we'll use the default value of MAXFILESIZE. Always do this, because user could change
            #this at any time. Best to always check and then use default if it is not set.
            MAXSIZE=MAXFILESIZE

        #force to int for compare because we have a lot of strings here...
        if (int(DBSIZE) > int(MAXSIZE)):
          syslog.syslog("toptalker DB at %s bytes, running cleanup." % "{:,}".format(DBSIZE))

          #How old do we want to delete our db entries?
          if self.agentMgr.agent_option("HOURSOLD"):
              MAXHOURS = self.agentMgr.agent_option("HOURSOLD")
          else:
              #Else we'll use the default value of HOURSOLD
              MAXHOURS=HOURSOLD

          #TODO would be a little cleaner to have DELETE and VACUUM as a function.
          #
          try:
              conn = sqlite3.connect ( SQLDBFILE )
              conn.row_factory = sqlite3.Row
              db = conn.cursor()
              rows = db.execute("DELETE from acct_v5 where stamp_updated <= datetime('now', '-%s hour');" % str(MAXHOURS))
              db.execute("VACUUM")
              conn.commit()
          except sqlite3.Error as e:
              syslog.syslog("%s" % e)
              syslog.syslog("Either db is corrupted or your sampling rate is too high. Deleting and creating a new db")
              #If we get here, then we have a serious issue with the database.
              #It could be corrupted, or we ran out of disk space. As a fail safe
              #method of dealing with this, we'll kill the sfacctd process, create a new
              #blank db file and then restart. We'll provide a detailed syslog message of the issue.
              #If filesystem is full (since we need more space for the VACUUM), then notify user
              #so they know they need to back off on their sflow sampling rate and be more conservative
              #with the db size and retention.
              self.kill_sfacctd()
              #sleep for 5 seconds just to let things stabilize. Before we create new db
              time.sleep(5)
              try:
                  os.remove(SQLDBFILE)
              except:
                  #We could use subprocess and use sudo as a sledgehammer
                  #but if we get here, its because somebody is manually tweaking files.
                  #If that is the case, its better to just error disable.
                  syslog.syslog("Unable to delete old db file. Shutting down agent.")
                  self.on_agent_enabled(enabled=False, reason='error disabled')

              #Create new db and restart
              self.create_db()
              self.start_sfacctd()
          finally:
              conn.close()

          syslog.syslog("Toptalker db cleanup task complete.")

        if self.agentMgr.agent_option("CHECKINTERVAL"):
          self.timeout_time_is(eossdk.now() + int(self.agentMgr.agent_option("CHECKINTERVAL")))
        else:
          self.timeout_time_is(eossdk.now() + int(CHECKINTERVAL))

    def on_agent_option(self, optionName, value):
        #options are a key/value pair
        if optionName == "CHECKINTERVAL":
          if not value:
              self.tracer.trace3("CHECKINTERVAL Deleted")
              self.agentMgr.status_set("CHECKINTERVAL:", CHECKINTERVAL)
          else:
              self.tracer.trace3("Adding CHECKINTERVAL %s" % value)
              self.agentMgr.status_set("CHECKINTERVAL:", "%s" % value)
        if optionName == "HOURSOLD":
          if not value:
              self.tracer.trace3("HOURSOLD Deleted")
              self.agentMgr.status_set("HOURSOLD:", HOURSOLD)
          else:
              self.tracer.trace3("Adding HOURSOLD %s" % value)
              self.agentMgr.status_set("HOURSOLD:", "%s" % value)
        if optionName == "MAXFILESIZE":
          if not value:
              self.tracer.trace3("MAXFILESIZE Deleted")
              self.agentMgr.status_set("MAXFILESIZE:", MAXFILESIZE)
          else:
              self.tracer.trace3("Adding MAXFILESIZE %s" % value)
              self.agentMgr.status_set("MAXFILESIZE:", "%s" % value)

    def on_agent_enabled(self, enabled,reason=None):
        #When shutdown set status and then shutdown
        if not enabled:
         self.tracer.trace0("Shutting down")
         self.agentMgr.status_del("Status:")
         if reason is not None:
             self.agentMgr.status_set("Status:", "Administratively Down - %s" % reason)
         else:
             self.agentMgr.status_set("Status:", "Administratively Down")
         syslog.syslog("Stopping toptalkers...")
         self.kill_sfacctd()

         self.agentMgr.agent_shutdown_complete_is(True)

    def start_sfacctd(self):
        #Check to see if sfacctd is running already. If it is, then don't start another instance
        #but return False. This is a fail safe so we don't keep respawning if sdk app has issues.
        #If sfacctd is not running, then we start it.
        #Use subprocess to start our sfacctd daemon
        import subprocess as sp
        process=sp.Popen("/bin/pgrep sfacctd", shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
        output, error = process.communicate()
        failed = process.returncode
        if not failed:
            #i.e. pgrep returned true
            syslog.syslog ("Toptalkers sflow collection daemon is already running. Using existing process.")
            return False
        else:
            syslog.syslog("Starting toptalkers sflow collection.")
            process=sp.Popen("sudo /usr/local/bin/sfacctd -D -f /etc/sfacctd.conf", shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
            output, error = process.communicate()
            failed = process.returncode
            if failed:
                syslog.syslog("Error starting sfacctd")
            return True

    def kill_sfacctd(self):
        #Use subprocess to do a sudo killall on all sfacctd processes
        # sudo /bin/killall sfacctd
        import subprocess as sp
        process=sp.Popen("sudo /bin/killall sfacctd", shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
        output, error = process.communicate()
        failed = process.returncode
        if failed:
            syslog.syslog("Error stopping sfacctd. Looks like process was not running.")
            return False
        return True

    def create_db(self):
        createtable =\
"""
CREATE TABLE acct_v5 (
	agent_id INT(8) NOT NULL DEFAULT 0,
	class_id CHAR(16) NOT NULL DEFAULT ' ',
	mac_src CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
	mac_dst CHAR(17) NOT NULL DEFAULT '0:0:0:0:0:0',
	vlan INT(4) NOT NULL DEFAULT 0,
	ip_src CHAR(15) NOT NULL DEFAULT '0.0.0.0',
	ip_dst CHAR(15) NOT NULL DEFAULT '0.0.0.0',
	src_port INT(4) NOT NULL DEFAULT 0,
	dst_port INT(4) NOT NULL DEFAULT 0,
	ip_proto CHAR(6) NOT NULL DEFAULT 0,
	tos INT(4) NOT NULL DEFAULT 0,
        packets INT NOT NULL,
	bytes BIGINT NOT NULL,
	flows INT NOT NULL DEFAULT 0,
	stamp_inserted DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
	stamp_updated DATETIME,
	PRIMARY KEY (agent_id, class_id, mac_src, mac_dst, vlan, ip_src, ip_dst, src_port, dst_port, ip_proto, tos, stamp_inserted)
);
"""
        try:
            conn = sqlite3.connect ( SQLDBFILE )
            conn.execute(createtable)
            conn.commit()
            conn.close()
        except Error as e:
            syslog.syslog("%s" % e)
            #If we get here, we should just shutdown so we don't just keep crashing
            #This could be someone changed directory permissions, etc.
            self.on_agent_enabled(enabled=False, reason='db creation error')
        finally:
            conn.close()
        #Change file ownership so we don't have any issues in the future.
        #Use subprocess so we can use sudo to do this. Yes, its the sledghammer approach...
        import subprocess as sp
        process=sp.Popen("sudo /bin/chown admin:eosadmin %s" % SQLDBFILE, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
        output, error = process.communicate()
        failed = process.returncode
        if failed:
            syslog.syslog("Error changing db file permissions.")
            self.on_agent_enabled(enabled=False, reason='setting db file ownership error')
            return False
        #Change file permissions so we don't have any issues in the future.
        #Use subprocess so we can use sudo to do this. Yes, its again the sledghammer approach...
        import subprocess as sp
        process=sp.Popen("sudo /bin/chmod 664 %s" % SQLDBFILE, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
        output, error = process.communicate()
        failed = process.returncode
        if failed:
            syslog.syslog("Error changing db file permissions.")
            self.on_agent_enabled(enabled=False, reason='setting db file permission error')
            return False
        return True

#=============================================
# MAIN
#=============================================
def main():
    syslog.openlog(ident="toptalkers-AGENT",logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL4)
    sdk = eossdk.Sdk()
    toptalkers = toptalkersAgent(sdk, sdk.get_timeout_mgr())
    sdk.main_loop(sys.argv)
    # Run the agent until terminated by a signal

if __name__ == "__main__":
    main()
