######################################################################
#
# UbiquitiSubscriberStation modeler plugin
#
######################################################################

__doc__="""UbiquitiSubscriberStation

UbiquitiSubscriberStation maps subscriber units on a Ubiquiti AP

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap, CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
#Ubiquiti data with -j is in json
import json

class UbiquitiSubscriberStation(CommandPlugin):

    #ssh modeling
    command = "echo -n `/sbin/discover -j`@@@SEPARATOR@@@`/usr/bin/wstalist`"

    relname = "ubiquitiSubscriberStation"
    modname = "ZenPacks.BCN.Ubiquiti.UbiquitiSubscriberStation"
    #get data from ZOPR 'getSSVolatileData', 'essid',
    deviceProperties = CommandPlugin.deviceProperties + ('getSSVolatileData',)
	   
    def process(self, device, results, log):
        """collect SSH information from this device"""
	#Log
        log.info('processing %s for device %s', self.name(), device.id)
        #JSON to py dict	
        tempDiscoveryData = json.loads(results.split('@@@SEPARATOR@@@')[0])['devices']
        discoveryData = {}
        for item in tempDiscoveryData:
            name = item.pop('hwaddr')
            discoveryData[name] = item
        
        #discoveryData = (dict(discoveryData[mydevice]['hwaddr'],discoveryData[mydevice]) for mydevice in discoveryData)
        wstalistData = json.loads(results.split('@@@SEPARATOR@@@')[1])
        #essid = getattr(device, 'essid', None)
	#volitiledata from Ubiquiti AP Device py
        volatiledata = getattr(device, 'getSSVolatileData', None)
	# Uncomment next lines for debugging when modeling
        log.debug( "Discovery Data= %s", discoveryData )
        log.debug ("Wstalist Data= %s", wstalistData )
	#log.info( "Device essid: %s ", essid)
	#log.info( "Volatile Data: %s", volatiledata)

	# If no data returned then simply return
        if ( not results ): 
                log.warn( 'No SSH response from %s for the %s plugin', device.id, self.name() )
                return

        ifIndex = 1

        rm = self.relMap()
        
	#Data to ZOPE
	#wmode 1:? 2:SS, 3:AP
	#hostname == System Service is AP
        for z in range(len(wstalistData)):
            try:
                om = self.objectMap()
                om.ssMAC = wstalistData[z]['mac']
                #keep data if SS is down check for existing data
                if (om.ssMAC in volatiledata) and len(volatiledata) > 0:
                   del volatiledata[om.ssMAC]
                if om.ssMAC in discoveryData:
                   om.ssDiscovery = "Enabled"
                   om.ssIPAddr = discoveryData[om.ssMAC]['ipv4']
                   om.ssDeviceName = discoveryData[om.ssMAC]['hostname']
                   om.ssProduct = discoveryData[om.ssMAC]['product']
                   om.ssFWversion = discoveryData[om.ssMAC]['fwversion']
                else:
                   om.ssDiscovery = "Disabled"
                   om.ssIPAddr = ""
                   om.ssDeviceName = wstalistData[z]['name']
                   if len(om.ssDeviceName) == 13:
                      om.ssDeviceName = om.ssDeviceName + "[...]"
                   om.ssProduct = ""
                   om.ssFWversion = ""
                om.id = self.prepId(om.ssMAC)
                om.ssDistance = wstalistData[z]['distance']
                om.snmpindex = self.hexToDotDec(om.ssMAC)
                om.ssStatus = 1

            except AttributeError, errorInfo:
                log.warn( " Attribute error in UbiquitiSubscriberStation modeler plugin %s", errorInfo)
                continue
               #Debug
               #log.info ("Appending data: %s", str(om))
	       #log.info ("Volatile data stack: %s", str(volatiledata))
            rm.append(om) 
        #Append data for SS which are down
	if len(volatiledata) > 0:
            for mac in volatiledata:
               try:
                   om = self.objectMap()
                   om.ssMAC = mac
                   om.ssIPAddr = volatiledata[mac]['ssIPAddr']
                   om.ssDeviceName = volatiledata[mac]['ssDeviceName']
                   om.ssProduct = volatiledata[mac]['ssProduct']
                   om.ssFWversion = volatiledata[mac]['ssFWversion']
                   om.ssDistance = volatiledata[mac]['ssDistance']
                   om.ssDiscovery = volatiledata[mac]['ssDiscovery']		
                   om.id = self.prepId(om.ssMAC)
                   om.snmpindex = self.hexToDotDec(om.ssMAC)
                   om.ssStatus = 0
               except AttributeError, errorInfo:
                   log.warn( " Attribute error in UbiquitiSubscriberStation modeler plugin %s", errorInfo)
                   continue
               #Debug
               #log.info ("Appending data: %s", str(om))
               rm.append(om)
        return rm
    #Dot dec to hex MAC NOT used
    def dotDecToHex(self,dotdec):
       mac = ""
       temp = dotdec.split('.')
       for i in range(1, 7):
          if (int(temp[i]) < 16):
             mac += "0" + hex(int(temp[i]))[2:] + ":"
 	  else:
	     mac += hex(int(temp[i]))[2:] + ":"
       mac = mac.upper()[:-1]
       return mac
    #MAC Hex to dotdec 5 is Wirless Ubiquiti interface
    def hexToDotDec(self,MacHex):
       MacDot = ""
       MacHex = MacHex.split(':')
       for i in range(0,6):
          MacDot +=  str(int(MacHex[i], 16))+'.'
	  if i == 5:
             MacDot += '5'
       return MacDot
