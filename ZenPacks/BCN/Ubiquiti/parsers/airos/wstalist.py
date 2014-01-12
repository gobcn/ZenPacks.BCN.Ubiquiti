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
        for dp in cmd.points:
            dp.component = dp.data['componentScanValue']
            points = ifs.setdefault(dp.component, {})
            points[dp.id] = dp

        # split data into component blocks
        parts = json.loads(cmd.result.output)

        for part in parts:
	    # find the component match
            component = part['mac']
            if self.componentScanValue == 'id': component = self.prepId(component)
            points = ifs.get(component, None)
            if not points: continue

            del part['signals']
	    del part['rates']

            part = flatten_dict(part)

            # find any datapoints
            for name, value in part.items():
                dp = points.get(name, None)
                if dp is not None:
                   if value in ('-', ''): value = 0
                   result.values.append( (dp, float(value) ) )

        #log.debug(pformat(result))
        return result

