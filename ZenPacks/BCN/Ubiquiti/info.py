# This file is the conventional place for "Info" adapters. Info adapters are
# a crucial part of the Zenoss API and therefore the web interface for any
# custom classes delivered by your ZenPack. Examples of custom classes that
# will almost certainly need info adapters include datasources, custom device
# classes and custom device component classes.

# Mappings of interfaces (interfaces.py) to concrete classes and the factory
# (these info adapter classes) used to create info objects for them are managed
# in the configure.zcml file.

from zope.component import adapts
from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.infos.template import RRDDataSourceInfo

from ZenPacks.BCN.Ubiquiti.UbiquitiSubscriberStation import UbiquitiSubscriberStation
from ZenPacks.BCN.Ubiquiti.interfaces import IUbiquitiSubscriberStationInfo


class UbiquitiSubscriberStationInfo(ComponentInfo):
    implements(IUbiquitiSubscriberStationInfo)
    adapts(UbiquitiSubscriberStation)

    monitor = ProxyProperty("monitor")
    snmpindex = ProxyProperty("snmpindex")
    ssMAC = ProxyProperty("ssMAC")
    ssIPAddr = ProxyProperty("ssIPAddr")
    ssDeviceName = ProxyProperty("ssDeviceName")
    ssProduct = ProxyProperty("ssProduct")
    ssFWversion = ProxyProperty("ssFWversion")
    ssStatus = ProxyProperty("ssStatus")
    ssDiscovery = ProxyProperty("ssDiscovery")
    firmware = ProxyProperty("firmware")
    distance = ProxyProperty("distance")

    @property
    def firmware(self):
        sufirmware = self._object.getFirmware()
        return sufirmware

    @property
    def distance(self):
        sudistance = self._object.getDistance()
        return sudistance
