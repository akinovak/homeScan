from pymongo import MongoClient


class MongoAdapter:
    def __init__(self, database_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[database_name]
        self.a = {'cena': 2000.0, 'cena_m2': 18, 'naselje': 'Hram Svetog Save (Vračar)', 'zona': 'Stambena zona', 'grejanje': 'Centralno grejanje', 'sprat': 'Namešten', 'parking': 'da', 'kuhinja': '1', 'dnevne': '1', 'kupatila': '1', 'wc': '1', 'dodatno': 'Luksuzno', 'objavljeno': '06/11/2019', 'azurirano': '17/12/2019', 'kod_sistema': '9140670', 'link': 'https://www.srbija-nekretnine.org/6980510', 'stanje': '', 'adresa': '', 'kod_oglasa': 0, 'nivoi': 0, 'tip': '', 'kvadratura': 112}

    def insert_one(self, o, collection):
        try:
            collection = self.db[collection]
            # collection.insert_one(self.a)
            # print('insertujem')
            print(o)
            collection.insert_one(o)
        except Exception as e:
            print(e)

    def update_one(self, obj_match, obj_update, collection):
        try:
            self.db[collection].update_one(obj_match, obj_update)
        except Exception as e:
            print(e)

    def delete_one(self, obj, collection):
        try:
            self.db[collection].delete_one(obj)
        except Exception as e:
            print(e)

    def find_one(self, obj, collection):
        try:
            return self.db[collection].find_one(obj)
        except Exception as e:
            print(e)
            return None

    def find(self, o, collection, limit):
        collection = self.db[collection]
        cursor = collection.find(o).limit(limit)
        return cursor
