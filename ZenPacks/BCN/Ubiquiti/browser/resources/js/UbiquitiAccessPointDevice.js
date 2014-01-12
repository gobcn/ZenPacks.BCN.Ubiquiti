/*
 * Based on the configuration in ../../configure.zcml this JavaScript will only
 * be loaded when the user is looking at a UbiquitiAccessPointDevice in the web interface.
 */

(function(){

var ZC = Ext.ns('Zenoss.component');


/*
 * Friendly names for the components. First parameter is the meta_type in your
 * custom component class. Second parameter is the singular form of the
 * friendly name to be displayed in the UI. Third parameter is the plural form.
 */
ZC.registerName('UbiquitiSubscriberStation', _t('Ubiquiti Subscriber Station'), _t('Ubiquiti Subscriber Stations'));


/*
 * Custom component grid panel. This controls the grid that gets displayed for
 * components of the type set in "componentType".
 */
ZC.UbiquitiSubscriberStationPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'ssDeviceName',
            componentType: 'UbiquitiSubscriberStation',
            sortInfo: {
                field: 'ssDeviceName',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},
                {name: 'snmpindex'},
                {name: 'ssDeviceName'},
                {name: 'ssIPAddr'},
                {name: 'ssMAC'},
                {name: 'ssProduct'},
                {name: 'firmware'},
                {name: 'distance'},
                {name: 'ssDiscovery'},
		{name: 'ssStatus'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },/*{ 
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
                width: 50
            },*/{
                id: 'ssDeviceName',
                dataIndex: 'ssDeviceName',
                header: _t('Device Name'),
                sortable: true,
                width: 200
            },{
                id: 'ssIPAddr',
                dataIndex: 'ssIPAddr',
                header: _t('SS Management IP'),
                sortable: true,
                width: 120
            },{
                id: 'ssMAC',
                dataIndex: 'ssMAC',
                header: _t('SS MAC Address'),
                sortable: true,
                width: 120
            },{
                id: 'ssProduct',
                dataIndex: 'ssProduct',
                header: _t('Product'),
                sortable: true,
                width: 120
            },{
                id: 'firmware',
                dataIndex: 'firmware',
                header: _t('FW Version'),
                sortable: true,
                width: 90
            },{
                id: 'distance',
                dataIndex: 'distance',
                header: _t('SS Distance'),
                sortable: true,
                width: 75
            },{
                id: 'ssDiscovery',
                dataIndex: 'ssDiscovery',
                header: _t('Discovery'),
                sortable: true,
                width: 75
            },{
                id: 'ssStatus',
                dataIndex: 'ssStatus',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus, 
			/*function(ssS) {
                             if (ssS==1) {
                               return Zenoss.render.pingStatus('up');
                             } else {
                               return Zenoss.render.pingStatus('down');
                             }
                },*/
                width: 80,
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                width: 72,
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.UbiquitiSubscriberStationPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('UbiquitiSubscriberStationPanel', ZC.UbiquitiSubscriberStationPanel);

})();
