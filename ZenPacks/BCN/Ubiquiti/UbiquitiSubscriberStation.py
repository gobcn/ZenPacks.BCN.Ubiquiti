from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class UbiquitiSubscriberStation(DeviceComponent, ManagedEntity):
    meta_type = portal_type = "UbiquitiSubscriberStation"

    # Attributes specific to this component
    ssMAC = ''
    ssIPAddr=''
    ssDeviceName=''
    ssProduct=''
    ssFWversion=''
    ssStatus=0
    ssDistance=0
    ssDiscovery=''

    _properties = ManagedEntity._properties + (
        {'id': 'ssMAC', 'type': 'string', 'mode': ''},
        {'id': 'ssIPAddr', 'type': 'string', 'mode': ''},
	{'id': 'ssDeviceName', 'type': 'string', 'mode': ''},
	{'id': 'ssProduct', 'type': 'string', 'mode': ''},
	{'id': 'ssFWversion', 'type': 'string', 'mode': ''},
	{'id': 'ssStatus', 'type': 'int', 'mode': ''},
        {'id': 'ssDistance', 'type': 'int', 'mode': ''},
        {'id': 'ssDiscovery', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('ubiquitiAccessPointDevice', ToOne(ToManyCont,
            'ZenPacks.BCN.Ubiquiti.UbiquitiAccessPointDevice.UbiquitiAccessPointDevice',
            'ubiquitiSubscriberStation',
            ),
        ),
    )

    # Defining the "perfConf" action here causes the "Graphs" display to be
    # available for components of this type.
    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    def device(self):
        return self.ubiquitiAccessPointDevice()
    #Device status
    def getStatus(self):
        return self.ssStatus

    # remove extra info from ubiquiti firmware version
    def getFirmware(self):
       UbntVer = ""
       LongVer = self.ssFWversion.split('.')
       # in case long version has less than 5 elements, simply print whole thing
       if len(LongVer) < 5:
          UbntVer = LongVer
       # if minor revision greater than 15, it is probably build number instead
       elif (int(LongVer[4]) > 15):
          UbntVer = LongVer[2]+"."+LongVer[3]+".0"
       else:
          UbntVer = LongVer[2]+"."+LongVer[3]+"."+LongVer[4]
       return UbntVer

    def convertStatus(self, statusCode):
        if statusCode == 1:
           return "Up"
        else:
           return "Down"

    def getDistance(self):
        if self.ssDistance > 1000:
           return str(self.ssDistance/1000.0) + " km"
        elif self.ssDistance < 150:
           return "< 150 metres"
        else:
           return str(self.ssDistance) + " metres"

    def getInstDescription(self):
        return self.ssDeviceName

    #Sort fix
    #def primarySortKey(self):
    #"""Sort by Device Name then by MAC"""
       # return "%s" % (self.ssDeviceName)
    #Delete object
    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete ubiquitiSubscriberStation component
        """
        url = None
        if REQUEST is not None:
            url = self.device().ubiquitiSubscriberStation.absolute_url()
        self.getPrimaryParent()._delObject(self.id)

        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)



