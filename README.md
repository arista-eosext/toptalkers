# Toptalkers EOS Extension 

The purpose of this package is to provide an extension for Arista EOS that allows for local on switch
sflow sampling with integrated EOS CLI management and display of top talker traffic.

# Author
Jeremy Georges - Arista Networks   - jgeorges@arista.com

# Description
Toptalkers EOS Extension 

The purpose of this package is to provide an extension for Arista EOS switches that allows for local sflow 
sampling. Using the EOS SDK, this extension allows for control/management of the database and collection daemon so that
it is fully integrated in the CLI configuration. Additionally, the CLI has been extended so the top talker database can be
displayed natively in the CLI.

Although centralized sflow collection is the typical deployment model in most large networks, there is merit in supporting
some local sampling and providing that data natively in the switch CLI. The Toptalker extension satisfies the latter requirement
that some network operators like to have readily available.


## Example

### Output of 'show daemon' command
```
Agent: toptalkers (running with PID 2296)
Configuration:
Option              Value 
------------------- ----- 
CHECKINTERVAL       300    
HOURSOLD            12    
MAXFILESIZE         50000000 

Status:
Data                   Value                    
---------------------- ------------------------ 
CHECKINTERVAL:         300                       
DB SIZE (Bytes):       48,808,960               
HOURSOLD:              12                       
Last Check At:         Mon Dec 31 20:03:25 2018 
MAXFILESIZE:           50000000                    
Status:                Administratively Up      
```


```
Arista7010T-IDF#show toptalkers
Querying for Top Talkers. Please wait...
+-----------------+-----------------+-------------+---------------+----------+----------+----------+-----+
|      Src IP     |     Dest IP     | Total Bytes | Total Packets | Protocol | Src Port | Dst Port | TOS |
+-----------------+-----------------+-------------+---------------+----------+----------+----------+-----+
| 192.168.100.100 |  192.168.100.2  |   37455540  |     551629    |   udp    |   1000   |   2468   | 100 |
| 192.168.100.212 | 192.168.100.130 |   35569323  |     56511     |   tcp    |  59360   |   9910   |  0  |
| 192.168.100.213 | 192.168.100.130 |   32874185  |     51718     |   tcp    |  45081   |   9910   |  0  |
| 192.168.100.210 | 192.168.100.130 |   29221435  |     51813     |   tcp    |  57695   |   9910   |  0  |
| 192.168.100.214 | 192.168.100.130 |   16937319  |     30916     |   tcp    |  46825   |   9910   |  0  |
| 192.168.100.201 | 192.168.100.130 |   11333329  |     25699     |   tcp    |  45414   |   9910   |  0  |
| 192.168.100.200 | 192.168.100.130 |   11155341  |     25742     |   tcp    |  45151   |   9910   |  0  |
| 192.168.100.130 |  192.168.100.2  |   7780697   |     82866     |   tcp    |   9910   |  57707   |  0  |
| 208.111.155.246 |    10.0.0.117   |   7386345   |      5240     |   tcp    |   443    |  49803   |  32 |
|   13.107.4.50   |    10.0.0.97    |   5789445   |      3824     |   tcp    |    80    |  61184   |  32 |
| 192.168.100.130 | 192.168.100.212 |   3453404   |     31008     |   tcp    |   9910   |  59360   |  0  |
| 192.168.100.130 | 192.168.100.210 |   3329091   |     29852     |   tcp    |   9910   |  57695   |  0  |
| 192.168.100.130 | 192.168.100.213 |   3162380   |     28383     |   tcp    |   9910   |  45081   |  0  |
|    10.0.0.36    |     10.0.0.2    |   3088428   |      4023     |   tcp    |   3557   |   8081   |  0  |
| 192.168.100.130 | 192.168.100.214 |   1858118   |     16177     |   tcp    |   9910   |  46825   |  0  |
| 192.168.100.130 | 192.168.100.201 |   1750823   |     15448     |   tcp    |   9910   |  45414   |  0  |
| 192.168.100.130 | 192.168.100.200 |   1731280   |     15196     |   tcp    |   9910   |  45151   |  0  |
|     10.0.0.1    |     10.0.0.2    |   1347338   |      3347     |   udp    |  29602   |   514    |  0  |
|    10.0.0.20    |     10.0.0.2    |   1328215   |      3248     |   udp    |   5406   |  10650   |  0  |
|     10.0.0.2    |    10.0.0.254   |    948034   |      1646     |   icmp   |    0     |    0     | 192 |
|  172.217.14.206 |    10.0.0.117   |    743127   |      738      |   tcp    |   443    |  49537   |  32 |
|    10.0.0.131   |    10.0.0.133   |    611671   |      8451     |   tcp    |  37252   |  55443   |  0  |
|    10.0.0.133   |    10.0.0.131   |    595071   |      8278     |   tcp    |  55443   |  37249   |  0  |
|     10.0.0.2    |    10.0.0.20    |    578733   |      1352     |   icmp   |    0     |    0     | 192 |
|  216.58.194.174 |    10.0.0.117   |    559302   |      757      |   udp    |   443    |  52222   |  32 |
|    10.0.0.132   |    10.0.0.133   |    546728   |      8157     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.134   |    10.0.0.133   |    545017   |      8073     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.130   |    10.0.0.133   |    533584   |      8046     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.133   |    10.0.0.134   |    532320   |      8027     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.133   |    10.0.0.132   |    530390   |      7931     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.18    |     10.0.0.2    |    527984   |      1152     |   tcp    |  52516   |   8081   |  0  |
|    10.0.0.133   |    10.0.0.130   |    519926   |      7891     |   udp    |  55444   |  55444   |  0  |
|    10.0.0.19    |     10.0.0.2    |    509936   |      1166     |   tcp    |  60831   |   8081   |  0  |
|  172.217.14.197 |    10.0.0.114   |    426474   |      375      |   tcp    |   443    |  60528   |  32 |
|    10.0.0.117   |  54.241.186.124 |    364887   |      1933     |   tcp    |  63725   |   443    |  0  |
|  192.168.101.2  |  192.168.101.1  |    314446   |      2961     |   tcp    |  55842   |   443    |  0  |
|  192.168.101.1  |  192.168.101.2  |    306868   |      2904     |   tcp    |  36617   |   443    |  0  |
| 216.115.100.123 |    10.0.0.114   |    305455   |      232      |   tcp    |   443    |  46560   |  32 |
|     10.0.0.2    |    10.0.0.36    |    289362   |      3642     |   tcp    |   8081   |   3556   |  0  |
|    10.0.0.29    |     10.0.0.2    |    276796   |      3952     |   tcp    |    80    |  43438   |  0  |
|  172.217.14.197 |    10.0.0.117   |    270631   |      389      |   tcp    |   443    |  49496   |  32 |
|     0.0.0.0     | 255.255.255.255 |    268538   |      651      |   udp    |    68    |    67    |  0  |
|  216.58.194.165 |    10.0.0.117   |    263390   |      582      |   tcp    |   443    |  49836   |  32 |
|    10.0.0.117   | 208.111.155.246 |    262659   |      2518     |   tcp    |  49803   |   443    |  0  |
|    10.0.0.117   |  216.58.194.165 |    261276   |      626      |   tcp    |  49836   |   443    |  0  |
|     10.0.0.2    |    10.0.0.31    |    251118   |      813      |   icmp   |    0     |    0     | 192 |
|     10.0.0.2    |    10.0.0.42    |    248114   |      431      |   tcp    |   3128   |  54054   |  0  |
|  172.231.0.100  |    10.0.0.117   |    241440   |      160      |   tcp    |   443    |  49795   |  32 |
|     10.0.0.2    |    10.0.0.33    |    232924   |      743      |   icmp   |    0     |    0     | 192 |
|    10.0.0.33    |     10.0.0.2    |    225922   |      788      |   udp    |   2250   |  43251   |  0  |
+-----------------+-----------------+-------------+---------------+----------+----------+----------+-----+
```


### Syslog Messages
```
Installation of RPM
-------------------
Dec 30 00:48:09 localhost python: %EXTENSION-6-INSTALLING: Installing extension toptalkers-1.4.0-1.i386.rpm, version 1.4.0, SHA-1 554f076d11c1d6b189646dd251fca7f994e81831
Dec 30 00:48:09 localhost python: %EXTENSION-6-INSTALLED: Extension toptalkers-1.4.0-1.i386.rpm has been installed.
.
.
Starting of Agent
-----------------
Dec 30 00:51:02 localhost Launcher: %LAUNCHER-6-PROCESS_START: Configuring process 'toptalkers' to start in role 'ActiveSupervisor'
Dec 30 00:51:06 localhost toptalkers-AGENT[2296]: %AGENT-6-INITIALIZED: Agent 'toptalkers-toptalkers' initialized; pid=2296
Dec 30 00:51:06 localhost toptalkers-AGENT[2296]: toptalkers Initialized
Dec 30 00:51:06 localhost toptalkers-AGENT[2296]: Starting toptalkers sflow collection.
.
.
Agent running database garbage collection
-----------------------------------------
Dec 30 08:46:07 Arista7010T-IDF toptalkers-AGENT[2296]: toptalker DB at 40,069,120 bytes, running cleanup.
Dec 30 08:46:15 Arista7010T-IDF toptalkers-AGENT[2296]: Toptalker db cleanup task complete.
.
.
Agent Disk Full Recovery*
------------------------
Dec 31 01:02:03 Arista7010T-IDF toptalkers-AGENT[2296]: toptalker DB at 100,390,912 bytes, running cleanup.
Dec 31 01:02:14 Arista7010T-IDF toptalkers-AGENT[2296]: database or disk is full
Dec 31 01:02:14 Arista7010T-IDF toptalkers-AGENT[2296]: Either db is corrupted or your sampling rate is too high. Deleting and creating a new db
Dec 31 01:02:19 Arista7010T-IDF toptalkers-AGENT[2296]: Starting toptalkers sflow collection.
Dec 31 01:02:19 Arista7010T-IDF toptalkers-AGENT[2296]: Toptalker db cleanup task complete.
.
*If the database grows too large because of too high of a sample rate or retention settings are too long for the configured sample rate
the agent will remove the database and start with a clean/empty db. The reason for this is because sqlite needs additional
diskspace when executing a VACUUM. If there is not enough disk space to complete this action an error will occur. The error handling
is simply to stop the sfacctd daemon, recreate a new DB and restart the sflow collector.
```



# INSTALLATION:
Because toptalkers uses the latest sfacctd from the pmacct project (http://www.pmacct.net/) compiled with sqlite support in 32bit target, its best to just install
toptalkers with the RPM. The RPM includes all the TopTalker support files, sfacctd/pmacctd and the EOS SDK agent.


1. Copy the latest toptalker RPM to extensions: 
```
e.g. copy http://a-server-somewhere/toptalkers-1.4.0-1.i386.rpm extension:
```

2. Install extension
```
AristaSwitch#extension toptalkers-1.4.0-1.i386.rpm
```

3. Verify
```
AristaSwitch#show extensions 
Name                                  Version/Release      Status      Extension
------------------------------------- -------------------- ----------- ---------
toptalkers-1.4.0-1.i386.rpm           1.4.0/1              A, I        1        

A: available | NA: not available | I: installed | NI: not installed | F: forced
```

4. Make it auto install on reboot
```
AristaSwitch#copy installed-extensions boot-extensions
```


Add the following configuration snippets to change the default behavior.
```
!
daemon toptalkers
   exec /usr/local/bin/toptalkers
   option CHECKINTERVAL value 1800
   option HOURSOLD value 12
   option MAXFILESIZE value 50000000
   no shutdown
!
```

```
Config Option explanation:
   -CHECKINTERVAL is the time in seconds in which toptalker agent will check the file
    size of the database. Default time is 1800 seconds (30min).
   -MAXFILESIZE is the max file size in bytes of the database before clean up occurs.
    Default value is 50,000,000 (50MB)
   -HOURSOLD is the time in hours to use to clean up old entries. Default is 12 hours
    which means that when MAXFILESIZE is reached, all entries older than 12 hours (HOURSOLD)
    will be deleted and sqlite db will execute VACUUM to reduce file size.
```
Please note, if you do not specify options CHECKINTERVAL, HOURSOLD, or MAXFILESIZE in the configuration, the default values will be used.
Its best to be conservative in your values if you choose to over ride the defaults so that you do not consume excessive filesystem space.



To send sflow samples to the local collector, define the loopback as one of the sflow targets.
```
!
sflow sample 5000 #Whatever is appropriate for your use case 
sflow destination 127.0.0.1
sflow source-interface Vlan10 #Whatever is appropriate for your use case
sflow run
!
```

So, now your collector should be running and collecting sflow samples. How do you view this data that is being collected? 
This extension adds a new CliPlugin 'show toptalkers' which does this. 
Please note, because of the EOS CliPlugin framework, you must do a **'bash sudo killall ConfigAgent'**
in order for the new plugin to be registered. This will cause your *current* CLI session to terminate, so you'll have to log back into the switch.
If you reboot the switch and the RPM is also in boot-extensions, then you do NOT need to kill ConfigAgent as the CLI Extension is registered after a reboot.

# LIMITATIONS:
This release has been tested on EOS 4.20.1, 4.20.10, 4.21.2. Please test this extension on future releases of EOS **before** using this in production as this has 
specific target compiled binaries for these specific EOS releases and may change in the future.
Also, this release has not been tested on MLAG or multi-supervisor platforms, nor with hardware-accelerated sFlow.

# FILE STRUCTURE DETAIL:
Most of the following detail can be ignored if you are installing toptalkers from the included RPM. The details below are included for those that may want to modify
the extension or support files.

The main EOS SDK agent and wrapper for the sfacctd sflow collector is '/usr/local/bin/toptalkers.py'. Because Sysdb mountprofiles are needed to match the name of the SDK
application, the RPM will install the file without the .py extension. The matching toptalkers.sysdb is also moved during the RPM installation to the /usr/lib/SysdbMountProfiles/
directory and the file extension is removed.

sfacctd.conf is copied to the /etc directory and must be in this location. Additionally, this configuration file includes which sflow sample data is aggregated and where
the sqlite db path resides.

The actual database is /tmp/sampling.db. On Arista platforms, /tmp is limited in space because it is in RAM. Therefore, several exception handling routines are used 
to address this space constraint. It also means that users need to be careful in how high of a sample rate they are using coupled with the retention times configured. 
If space becomes unavailabe, we use the sledgehammer approach and just remove the database file and build a new empty one. This is not ideal, but it is the most
stabile approach to deal with the limited disk space.

The TopTalkersCli.py is the CliPlugin that extends the EOS CLI to provide the 'show toptalkers' command. This file is copied over to the /usr/lib/python2.7/site-packages/CliPlugin/
directory.

Although pmacctd is not used with this extension, it was included with the RPM build for future use.

  

License
=======
BSD-3, See LICENSE file
