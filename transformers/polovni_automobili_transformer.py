import math
import re

class PolovniAutomobiliTransformer:

    def __init__(self, transform_map, def_map):
        self.transform_map = transform_map
        self.def_map = def_map

    def _transform_func(self, o):
        for k in list(o.keys()):
            self._transform_key(o, k)

    def _transform_key(self, o, k):
        o[self.transform_map[k]] = o[k]
        del o[k]

    def _set_def(self, o):
        for (k, v) in self.def_map.items():
            if k not in o.keys():
                o[k] = v

    def _clean_up(self, o):
        since = re.search('([0-9]*).', o['godiste'])
        if since is not None:
            o["godiste"] = int(since.group(1))

        cub = re.search('([0-9]*) cm', o['kubikaza'])
        if cub is not None:
            o["kubikaza"] = int(cub.group(1))

        km1 = re.search('([0-9]*)\.?[0-9]* km', o['kilometraza'])
        km2 = re.search('[0-9]*\.([0-9]*) km', o['kilometraza'])
        if km1 is not None:
            if km2 is not None:
                o["kilometraza"] = int(km1.group(1)) * 1000 + int(km2.group(1))
            else:
                o["kilometraza"] = int(km1.group(1))

        power = re.search('([0-9]*)\/([0-9]*) \(kW\/KS\)', o['snaga'])
        if (power != None):
            o["snaga"] = int(power.group(2))

    def transform(self, o):
        self._transform_func(o)
        self._set_def(o)
        self._clean_up(o)
        return o
