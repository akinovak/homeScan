from datetime import datetime, date
from random import randrange


class MongoRepository:
    def __init__(self, mongo_adapter):
        self.mongo_adapter = mongo_adapter

    def _prepare_insert(self, o):
        to_insert = {'link': o['link'], 'date': datetime.today().replace(hour=0, minute=0, second=0, microsecond=0), 'price': o['cena']}
        return to_insert

    def _prepare_string(self):
        return str(date.today()) + str(randrange(20, 40))

    def handle_object(self, o, collection):
        found = self.mongo_adapter.find_one({'link': o['link']}, collection)
        if found:
            self.mongo_adapter.update_one(
                {'link': o['link']},
                {'$set': {'cena': o['cena']}}, collection)
        else:
            self.mongo_adapter.insert_one(o, collection)
        self.mongo_adapter.insert_one(self._prepare_insert(o), 'test_cene')
