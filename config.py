from transformers.srbija_nekretnine_transformer import SrbijaNekretnineTransformer
from transformers.polovni_automobili_transformer import PolovniAutomobiliTransformer
from adapters.mongo_adapter import MongoAdapter
from repository.mongo_repository import MongoRepository


class Ctx:
    def __init__(self):
        self.transform_map = {
            'Adresa': 'adresa',
            'Cena': 'cena',
            'Cena po m2': 'cena_m2',
            'Naselje': 'naselje',
            'Zona': 'zona',
            'Način grejanja': 'grejanje',
            'Sprat': 'sprat',
            'Kuhinje': 'kuhinja',
            'Kupatila': 'kupatila',
            'Stanje': 'sprat',
            'Dodatno': 'dodatno',
            'Objavljeno': 'objavljeno',
            'Zadnje ažurirano': 'azurirano',
            'Parking mesto': 'parking',
            'Kod sistema': 'kod_sistema',
            'Kod oglasa': 'kod_oglasa',
            'Dnevne sobe': 'dnevne',
            'WC': 'wc',
            'Nivoi': 'novoi',
            'Tip': 'tip',
            'Link': 'link'
        }

        self.default_map = {
            'cena': 0,
            'cena_m2': 0,
            'naselje': '',
            'zona': '',
            'grejanje': '',
            'sprat': 0,
            'kuhinja': 0,
            'kupatila': 0,
            'stanje': '',
            'dodatno': '',
            'objavljeno': '',
            'azurirano': '',
            'adresa': '',
            'parking': '',
            'kod_sistema': 0,
            'kod_oglasa': 0,
            'dnevne': 0,
            'wc': 0,
            'nivoi': 0,
            'tip': '',
            'link': ''

        }

        self.pa_transform_map = {
            'Model': 'model',
            'Marka': 'marka',
            'Link': 'link',
            'Cena': 'cena',
            'Godište': 'godiste',
            'Karoserija': 'karoserija',
            'Gorivo': 'gorivo',
            'Kubikaža': 'kubikaza',
            'Snaga motora': 'snaga',
            'Kilometraža': 'kilometraza',
            'Emisiona klasa motora': 'emisiona_klasa_motora',
            'Pogon': 'pogon',
            'Menjač': 'menjac',
            'Vozilo:': 'vozilo',
            'Mesto': 'mesto'
        }

        self.pa_default_map = {
            'model': '',
            'marka': '',
            'link': '',
            'cena': '',
            'godiste': 0,
            'snaga': 0,
            'gorivo': '',
            'kubikaza': '',
            'kilometraza': 0,
            'emisiona_klasa_motora': '',
            'pogon': '',
            'menjac': '',
            'vozilo': '',
            'mesto': ''
        }

        self.user_agents = [
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/57.0.2987.110 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.79 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
             'Gecko/20100101 '
             'Firefox/55.0'),  # firefox
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.91 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/62.0.3202.89 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/63.0.3239.108 '
             'Safari/537.36'),  # chrome
        ]

        self.sn_transformer = SrbijaNekretnineTransformer(self.transform_map, self.default_map)
        self.pa_transformer = PolovniAutomobiliTransformer(self.pa_transform_map, self.pa_default_map)
        self.mongo_adapter = MongoAdapter('Polovni')
        self.mongo_repository = MongoRepository(self.mongo_adapter)


ctx = Ctx()
