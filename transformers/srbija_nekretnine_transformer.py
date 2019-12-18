import math


class SrbijaNekretnineTransformer:

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
        ind = o['cena'].rfind('\n')
        if not ind == -1:
            o['cena'] = o['cena'][:o['cena'].rfind('\n')]
        o['cena_m2'] = int(o['cena_m2'][o['cena_m2'].rfind(' ') + 1:])
        if '.' in o['cena']:
            o['cena'] = float(o['cena'])*1000
        else:
            o['cena'] = float(o['cena'])
        o['kvadratura'] = math.ceil(o['cena']/o['cena_m2'])
    def transform(self, o):
        self._transform_func(o)
        self._set_def(o)
        self._clean_up(o)
        return o
