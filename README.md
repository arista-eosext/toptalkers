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

# New Features
Added in this release is parsing sFlow samples with VLAN and ingress Interface information and adding this to the database and output of the 'show toptalkers' command.

Additionally, all sampled flows can now be displayed by by using the 'all' keyword with 'show toptalkers all'. Without the 
'all' parameter, only the top 50 flows are displayed.

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
+-----------------+-----------------+------+---------+-------------+---------------+----------+----------+----------+-----+
|      Src IP     |     Dest IP     | VLAN | In Intf | Total Bytes | Total Packets | Protocol | Src Port | Dst Port | TOS |
+-----------------+-----------------+------+---------+-------------+---------------+----------+----------+----------+-----+
|    10.0.0.34    |     10.0.0.2    |  10  |    1    |    500459   |      458      |   tcp    |   4136   |    20    |  0  |
| 192.168.100.214 | 192.168.100.130 | 192  |    2    |    209820   |      387      |   tcp    |  50403   |   9910   |  0  |
| 192.168.100.221 | 192.168.100.130 | 192  |    2    |    196321   |      515      |   tcp    |  58156   |   9910   |  0  |
| 192.168.100.200 | 192.168.100.130 | 192  |    2    |    107088   |      264      |   tcp    |  40914   |   9910   |  0  |
| 192.168.100.201 | 192.168.100.130 | 192  |    2    |    93319    |      286      |   tcp    |  46060   |   9910   |  0  |
| 192.168.100.130 |  192.168.100.2  | 192  |    5    |    89938    |      925      |   tcp    |   9910   |  50002   |  0  |
|  192.168.100.17 | 192.168.100.130 | 192  |    14   |    54921    |      282      |   tcp    |  36080   |   9910   |  0  |
|  192.168.100.5  | 192.168.100.130 | 192  |    14   |    54620    |      277      |   tcp    |  36156   |   9910   |  0  |
|  192.168.100.16 | 192.168.100.130 | 192  |    14   |    54103    |      284      |   tcp    |  33020   |   9910   |  0  |
|  192.168.100.13 | 192.168.100.130 | 192  |    14   |    53652    |      271      |   tcp    |  45598   |   9910   |  0  |
|  192.168.100.19 | 192.168.100.130 | 192  |    14   |    53375    |      255      |   tcp    |  56948   |   9910   |  0  |
|  192.168.100.15 | 192.168.100.130 | 192  |    14   |    53199    |      260      |   tcp    |  60290   |   9910   |  0  |
|  192.168.100.7  | 192.168.100.130 | 192  |    14   |    53147    |      260      |   tcp    |  49976   |   9910   |  0  |
|  192.168.100.20 | 192.168.100.130 | 192  |    14   |    53106    |      263      |   tcp    |  60706   |   9910   |  0  |
|  192.168.100.14 | 192.168.100.130 | 192  |    14   |    52175    |      259      |   tcp    |  36318   |   9910   |  0  |
|  192.168.100.18 | 192.168.100.130 | 192  |    14   |    51049    |      258      |   tcp    |  38804   |   9910   |  0  |
|  192.168.100.12 | 192.168.100.130 | 192  |    14   |    50394    |      233      |   tcp    |  53084   |   9910   |  0  |
|  192.168.100.9  | 192.168.100.130 | 192  |    14   |    49447    |      238      |   tcp    |  42466   |   9910   |  0  |
|  192.168.100.8  | 192.168.100.130 | 192  |    14   |    48891    |      233      |   tcp    |  60464   |   9910   |  0  |
|  192.168.100.10 | 192.168.100.130 | 192  |    14   |    46957    |      211      |   tcp    |  51130   |   9910   |  0  |
|  192.168.100.6  | 192.168.100.130 | 192  |    14   |    46925    |      203      |   tcp    |  39074   |   9910   |  0  |
|  192.168.100.11 | 192.168.100.130 | 192  |    14   |    44335    |      176      |   tcp    |  52474   |   9910   |  0  |
| 192.168.100.130 | 192.168.100.221 | 192  |    5    |    38670    |      345      |   tcp    |   9910   |  58156   |  0  |
|     10.0.0.2    |    10.0.0.34    |  10  |    11   |    28781    |      381      |   tcp    |    20    |   4136   |  8  |
|   50.126.87.18  |    10.0.0.114   |  10  |    1    |    27356    |       30      |   tcp    |   8022   |  54848   |  32 |
| 192.168.100.130 | 192.168.100.214 | 192  |    5    |    24469    |      217      |   tcp    |   9910   |  50403   |  0  |
| 192.168.100.130 |  192.168.100.16 | 192  |    5    |    22959    |      180      |   tcp    |   9910   |  33020   |  0  |
|  54.153.116.159 |    10.0.0.117   |  10  |    1    |    22716    |       42      |   tcp    |   443    |  59651   |  32 |
| 192.168.100.130 |  192.168.100.17 | 192  |    5    |    22625    |      176      |   tcp    |   9910   |  36080   |  0  |
| 192.168.100.130 |  192.168.100.5  | 192  |    5    |    22277    |      174      |   tcp    |   9910   |  36156   |  0  |
| 192.168.100.130 |  192.168.100.13 | 192  |    5    |    21760    |      170      |   tcp    |   9910   |  45598   |  0  |
|     10.0.0.1    |     10.0.0.2    |  10  |    1    |    21674    |       50      |   udp    |  58491   |   514    |  0  |
| 192.168.100.130 |  192.168.100.20 | 192  |    5    |    21664    |      171      |   tcp    |   9910   |  60706   |  0  |
| 192.168.100.130 |  192.168.100.7  | 192  |    5    |    21427    |      169      |   tcp    |   9910   |  49976   |  0  |
| 192.168.100.130 |  192.168.100.18 | 192  |    5    |    21346    |      169      |   tcp    |   9910   |  38804   |  0  |
| 192.168.100.130 |  192.168.100.15 | 192  |    5    |    21124    |      166      |   tcp    |   9910   |  60290   |  0  |
| 192.168.100.130 |  192.168.100.14 | 192  |    5    |    20864    |      163      |   tcp    |   9910   |  36318   |  0  |
| 192.168.100.130 | 192.168.100.201 | 192  |    5    |    20743    |      179      |   tcp    |   9910   |  46060   |  0  |
| 192.168.100.130 |  192.168.100.9  | 192  |    5    |    20578    |      167      |   tcp    |   9910   |  42466   |  0  |
| 192.168.100.130 |  192.168.100.19 | 192  |    5    |    20510    |      160      |   tcp    |   9910   |  56948   |  0  |
| 192.168.100.130 | 192.168.100.200 | 192  |    5    |    20133    |      182      |   tcp    |   9910   |  40914   |  0  |
| 192.168.100.130 |  192.168.100.12 | 192  |    5    |    19585    |      154      |   tcp    |   9910   |  53084   |  0  |
| 192.168.100.130 |  192.168.100.8  | 192  |    5    |    19164    |      151      |   tcp    |   9910   |  60464   |  0  |
|  17.252.226.85  |    10.0.0.117   |  10  |    1    |    18866    |       33      |   tcp    |   443    |  59647   |  32 |
|    10.0.0.20    |     10.0.0.2    |  10  |    1    |    17803    |       43      |   udp    |   5288   |  43089   |  0  |
| 192.168.100.130 |  192.168.100.10 | 192  |    5    |    17285    |      136      |   tcp    |   9910   |  51130   |  0  |
| 192.168.100.130 |  192.168.100.6  | 192  |    5    |    17115    |      136      |   tcp    |   9910   |  39074   |  0  |
|    10.0.0.20    |     10.0.0.3    |  10  |    1    |    15162    |       36      |   udp    |   5162   |  54784   |  0  |
| 192.168.100.130 |  192.168.100.11 | 192  |    5    |    14689    |      117      |   tcp    |   9910   |  52474   |  0  |
|     10.0.0.2    |    10.0.0.254   |  10  |    11   |    14154    |       25      |   icmp   |    0     |    0     | 192 |
+-----------------+-----------------+------+---------+-------------+---------------+----------+----------+----------+-----+
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
e.g. copy http://a-server-somewhere/toptalkers-1.5.0-1.i386.rpm extension:
```

2. Install extension
```
AristaSwitch#extension toptalkers-1.5.0-1.i386.rpm
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

5. Add the following configuration snippets to change the default behavior.
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


# Upgrading
If upgrading from a previous release:

1. Shutdown the daemon first by issuing a 'shutdown' under the 'daemon toptalkers' configuration hierarchy.
2. Remove old extension by issuing a 'no extension \<*old-rpm-name*\>'
3. Delete the old extension by using 'delete extension \<*old-rpm-name*\>'
4. Follow steps 1-4 in above installation instructions.


# LIMITATIONS:
This release has been tested on EOS 4.20.1, 4.20.10, 4.20.12M, 4.21.2, 4.22.0F.  
Please test this extension on future releases of EOS **before** using this in production as this has  
specific target compiled binaries for these specific EOS releases and may change in the future.  
Also, this release has not been tested on MLAG or multi-supervisor platforms, nor with hardware-accelerated sFlow.  

If an sflow sample includes a non-front panel interface (such as a Port-channel, etc) the interface shown in the toptalker  
output will usually be a large number. For example, 'interface port-channel 1' will typically be 1000001 and port-channel 2  
will be 1000002. This corresponds to the SNMP index of the interface. The native EOS sFlow agent uses this in the sFlow  
header and toptalkers is just displaying what is sent in that header. To see which interface a particular index maps to  
you can use the command 'show snmp mib ifmib ifindex'. Additionally, if an interface is a routed port  
(i.e. 'no switchport') the VLAN field will show as 'N/A' in the toptalker output.

Based on licensing, this is Open Source and this and other Open Source tools are not supported directly by  
Arista Support. Support is best effort as it relates to extensions such as this one.  

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
If space becomes unavailable, we use the sledgehammer approach and just remove the database file and build a new empty one. This is not ideal, but it is the most
stable approach to deal with the limited disk space.

The TopTalkersCli.py is the CliPlugin that extends the EOS CLI to provide the 'show toptalkers' command. This file is copied over to the /usr/lib/python2.7/site-packages/CliPlugin/
directory.

Although pmacctd is not used with this extension, it was included with the RPM build for future use.

  

License
=======
BSD-3, See LICENSE file
