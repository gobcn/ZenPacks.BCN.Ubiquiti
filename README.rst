=====================
ZenPacks.BCN.Ubiquiti
=====================

.. contents::
   :depth: 3

This project is a Zenoss_ extension (ZenPack) that allows for monitoring of
Ubiquiti Access Points and Subscriber Stations.

Requirements & Dependencies
---------------------------
This ZenPack is known to be compatible with Zenoss version 3.2.1.

Installation
------------
You must first have, or install, Zenoss 3.2.1. Core and Enterprise
versions are supported. You can download the free Core version of Zenoss from
http://community.zenoss.org/community/download .

Normal Installation (packaged egg)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Depending on what version of Zenoss you're running you will need a different
package. Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 3.2.1: `Latest Package for Python 2.6`_

Then copy it to your Zenoss server and run the following commands as the zenoss
user::

    zenpack --install <package.egg>
    zenoss restart

Developer Installation (link mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you wish to further develop and possibly contribute back you should clone
the git repository, then install the ZenPack in developer mode using the
following commands::

    git clone git://github.com/gobcn/ZenPacks.BCN.Ubiquiti.git
    zenpack --link --install ZenPacks.BCN.Ubiquiti
    zenoss restart

Usage
-----
Installing the ZenPack will add the following objects to your Zenoss system.

* Device Classes

  * /Devices/Network/Wireless/Ubiquiti/airMAX AP

* Monitoring Templates

  * UbiquitiAccessPoint in /Network/Wireless/Ubiquiti/airMAX AP
  * UbiquitiSubscriberStation in /Network/Wireless/Ubiquiti/airMAX AP

* Event Classes (each with transforms)

  * /Status/UbiquitiSubscriberStation

* MIBs

  * /mibs/FROGFOOT-RESOURCES-MIB
  * /mibs/MIKROTIK-EXPERIMENTAL-MIB

Access Point Monitoring
~~~~~~~~~~~~~~~~~~~~~~~
In addition to the interfaces graphs the following graphs are included:

* CPU Load Average 

  * For 1, 5, 15 minute in %

* Memory Utilization

  * RAM utilization Used, Buffered, Cached, and Free


Subscriber Unit Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~
The plugin adds a "Ubiquiti Subscriber Stations" component type under Components for devices in the airMAX AP class. The following fields are provided:

* Events - Shows active events for the SS
* Device Name - A string to describe the SS - set on the SS manually
* SS Management IP - IP address for the SS's management interface
* SS MAC Address - MAC address for the SS
* Product - A string to describe SS model 
* FW version - SS firmware version
* SS Distance - Distance to the SS in Meters or Kilometers
* Discovery - Indicates whether discovery is enabled or disabled on the SS
* Status - Custom status field for Up/Down status of SS
* Monitored - true/false to enable/disable monitoring
* Locking - component locking settings

The following graphs are provided for the Subscriber Stations:

* Throughput

  * Displays the current SS traffic. On the SS itself, due to the fact that the
    SS measures traffic from the POV of the Ethernet interface, the inbound
    counters represent the outbound traffic and the outbound counters represent 
    the inbound traffic; as a result, to make the graph more understandable,
    the graph itself has been inverted. Therefore, the Inbound graph correctly
    represents the AP-SS traffic and the Outbound graph correctly represents
    the SS-AP traffic.

* Packets

  * Displays the current packets/sec Inbound and Outbound on the SS

* Signal - RSSI

  * SS Signal Strength (dBm)
  * Noise Floor (dBm)

* CCQ

  * Displays the Client Connection Quality Percentage

* Theoretical Maximum Throughput at Current Modulation

  * Displays maximum transmit and receive speeds given modulation

* AirMax Quality and Capacity

  * Current AirMax Quality and Capacity in Percent

* Transmit Power

  * Current Transmit Power value

* ACK

  * Acknowledgement Timeout value

Status monitoring for subscriber stations is also provided. Active polling is
carried out, in addition to syslog messages parsing in a transform. 
A custom "Status" field was used for the status indicator rather than built-in 
status field due to the fact that the built in field uses events to determine 
up/down status.

The event transforms handle the various up/down states. If an SS goes up or down, 
the transforms will change the status attribute in the DMD for the SS and then 
commit the change. To prevent all of the "customer is offline" events from filling 
up the event console and making the device yellow, the transforms are configured 
to drop any event where the Device Name of the corresponding Subscriber Station does 
not start with "vip-". In this way, you can receive events for VIP customers without 
events being created for non-VIP customers. Up/Down status is handled before the 
event is dropped, for non-VIP SS's, ensuring that the Status attribute is set 
correctly before the event is deleted.

Known Issues
------------
Ubiquiti Access Points do not store any SS data in memory when the subscriber 
is disconnected. This led to an issue where a previously modeled subscriber's 
Device Name, IP, MAC address, Product and FW version would disappear if the 
subscriber happened to be offline during a modeling cycle. The SS would 
only reappear the next time a modeling cycle coincided with the subscriber 
being online. To work around this issue, this ZenPack is designed to read the 
prevous data from the DMD for customers who are offline during a model but 
previously modeled successfully.  

Automatic sorting of the list of Subscriber Stations by Device Name is not working.
Alphabetical sort is occuring, leading to wrong sorting. Clicking on the column
header for Device Name after opening the list causes it to sort correctly and 
can be used as a workaround until the cause of this issue is determined.

Screenshots
-----------
* |Subscriber Unit Monitoring|
* |Subscriber Unit Graphs|

Version History
---------------
* 1.02 - January 14, 2014 - Multiple bug fixes/enhancements
  * Uses wstalist instead of discover to model device
  * Adds discovery information if available (ex. firmware version, mgmt IP)
  * Uses wstalist instead of SNMP for graphing - now graphs CCQ, airmax, etc.
* 1.01 - August 15, 2012 - Initial Release

.. _Zenoss: http://www.zenoss.com/
.. _Latest Package for Python 2.6: https://github.com/downloads/gobcn/ZenPacks.BCN.Ubiquiti/ZenPacks.BCN.Ubiquiti-1.02-py2.6.egg

.. |Subscriber Unit Monitoring| image:: https://github.com/gobcn/ZenPacks.BCN.Ubiquiti/raw/master/docs/sumonitoring.png
.. |Subscriber Unit Graphs| image:: https://github.com/gobcn/ZenPacks.BCN.Ubiquiti/raw/master/docs/sugraphs.png
