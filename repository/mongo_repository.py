from datetime import date
from random import randrange

class MongoRepository:
    def __init__(self, mongo_adapter):
        self.mongo_adapter = mongo_adapter

    def _prepare_insert(self, o):
        to_insert = {}
        to_insert['link'] = o['link']
        to_insert['istorija'] = [{
            'date': str(date.today()),
            'price': o['cena']
        }]

        return to_insert

    def _prepare_string(self):
        return str(date.today()) + str(randrange(20, 40))

    def handle_object(self, o, collection):
        found = self.mongo_adapter.find_one({'link': o['link']}, collection)
        if found:
            self.mongo_adapter.update_one(
                {'link': o['link']},
                {'$set': {'cena': o['cena']}}, collection)
            self.mongo_adapter.update_one(
                {'link': o['link']},
                {'$push': {'istorija': {'date': self._prepare_string(), 'price': o['cena']}}}, 'test_cene')
        else:
            self.mongo_adapter.insert_one(o, collection)
            self.mongo_adapter.insert_one(self._prepare_insert(o), 'test_cene')
