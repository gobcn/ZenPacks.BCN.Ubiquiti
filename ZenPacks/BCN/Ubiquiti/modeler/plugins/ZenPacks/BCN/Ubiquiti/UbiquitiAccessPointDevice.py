######################################################################
#
# UbiquitiAccessPointDevice modeler plugin
#
######################################################################

__doc__="""UbiquitiAccessPointDevice

UbiquitiAccessPointDevice sets up hardware / software manufacturer
and sets other information.

$Id: $"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs

class UbiquitiAccessPointDevice(SnmpPlugin):
    maptype = "UbiquitiAccessPointDevice"
    
    snmpGetMap = GetMap({
        '.1.2.840.10036.1.1.1.9.5' :  'essid',
	'.1.2.840.10036.3.1.2.1.3.5': 'setHWProductKey',
	'.1.2.840.10036.3.1.2.1.2.5': 'setOSProductKey',
	'.1.2.840.10036.3.1.2.1.4.5': 'setOSVersion',
        })

    def condition(self, device, log):
        """only for boxes with proper object id"""
        return device.snmpOid.startswith(".1.3.6.1.4.1.10002.1")

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        
# Uncomment next 2 lines for debugging when modeling
        log.debug( "Get Data= %s", getdata )
        log.debug( "Table Data= %s", tabledata )
        try:
            om = self.objectMap(getdata)
	    om.setHWProductKey = MultiArgs(om.setHWProductKey, "Ubiquiti")
	    if om.setOSVersion is not None:
	       UbntVer = om.setOSVersion
	       UbntVer = UbntVer.split('.')
	       UbntVer = UbntVer[2]+'.'+UbntVer[3]
	       om.setOSProductKey =  'AirOS ' + UbntVer
	    else:
	       om.setOSProductKey = "Not available"

	    om.setOSProductKey = MultiArgs(om.setOSProductKey, "Ubiquiti")
            return om
        except:
            log.warn( " Error in getting data for UbiquitiAccessPointDevice modeler plugin" )

