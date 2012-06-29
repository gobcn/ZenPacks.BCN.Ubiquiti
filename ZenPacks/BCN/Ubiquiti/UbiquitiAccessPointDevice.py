from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class UbiquitiAccessPointDevice(Device):
    """
    UbiquitiAccessPointDevice device subclass.
    """

    meta_type = portal_type = 'UbiquitiAccessPointDevice'

    #If multiple APs are deployed, ESSID helps to group users under one AP.
    #This is done because in the process of SSH modeling all users from all
    #APs are pulled.

    essid = ''

    _properties = Device._properties + (
        {'id':'essid', 'type':'string', 'mode':''},
        )

    # This is where we extend the standard relationships of a device to add
    # our "UbiquitiSubscriberStation" relationship that must be filled with components
    # of our custom "UbiquitiSubscriberStation" class.
    # NOTE: class starts upper case; relationship starts lower case

    _relations = Device._relations + (
        ('ubiquitiSubscriberStation', ToManyCont(ToOne,
            'ZenPacks.BCN.Ubiquiti.UbiquitiSubscriberStation.UbiquitiSubscriberStation',
            'ubiquitiAccessPointDevice',
            ),
        ),
    )
    #http://community.zenoss.org/message/67078 very nice write up
    def getSSVolatileData(self):
        """Return the volatile data on existing SUs for modeler use"""
        myvolatiledata = {}
        for ss in self.ubiquitiSubscriberStation():
            ssinfo = { 'ssIPAddr' : ss.ssIPAddr, 'ssDeviceName' : ss.ssDeviceName, 'ssProduct' : ss.ssProduct, 'ssFWversion' : ss.ssFWversion }
            myvolatiledata[ss.ssMAC] = ssinfo
        return myvolatiledata

