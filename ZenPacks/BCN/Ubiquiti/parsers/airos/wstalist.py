from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

import json
from pprint import pformat

def flatten_dict(d):
    def items():
        for key, value in d.items():
           if isinstance(value, dict):
              for subkey, subvalue in flatten_dict(value).items():
                  yield key + "." + subkey, subvalue
           else:
                  yield key, value
    return dict(items())

class wstalist(ComponentCommandParser):

    def processResults(self, cmd, result):
        """
        Process the results of "wstalist" and separate the components.
        """

        # Map datapoints by data you can find in the command output
       
        ifs = {}
	# unitsdown is used to track up down status of subscriber unit
        unitsdown = []
        for dp in cmd.points:
            dp.component = dp.data['componentScanValue']
	    #assume all units are down by default
            if dp.component not in unitsdown:
               unitsdown.append(dp.component)
            points = ifs.setdefault(dp.component, {})
            points[dp.id] = dp

        #print "ifs is: " + str(ifs)

        # split data into component blocks
        parts = json.loads(cmd.result.output)

        for part in parts:
	    # find the component match
            component = part['mac']
            if self.componentScanValue == 'id': component = self.prepId(component)
            points = ifs.get(component, None)
            if not points: continue

			if 'signals' in part:
                del part['signals']
		    if 'rates' in part:
                del part['rates']

            part = flatten_dict(part)

            # if we are here it means the unit is up, so remove it from the down list
            if component in unitsdown: unitsdown.remove(component)
            # if unit is in list it is up, add fake value to results
            part['ss-status'] = 1 

            # find any datapoints
            for name, value in part.items():
                dp = points.get(name, None)
                if dp is not None:
                   if value in ('-', ''): value = 0
                   result.values.append( (dp, float(value) ) )

        #if ssstatus == 1:
        # anything left over has to be down
        for unit in unitsdown:
            points = ifs.get(unit, None)
            if not points: continue
	    dp = points.get('ss-status', None)
	    if dp is not None:
               result.values.append( (dp, 0.0) )

#log.debug(pformat(result))
        return result

