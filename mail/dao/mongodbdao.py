from pymongo import Connection
from json import dumps

class MongoDBDao(object):
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        connection = Connection(self.config.DB['Host'], int(self.config.DB['Port']))
        self.db = connection[self.config.DB['Name']]
        self.collection = self.db[self.config.DB['Collection']]

    def save(self, obj):
        doc = self.collection.find_one({ '_id': obj['_id'] })

        if doc is not None:
            return

        try:
            self.collection.insert(obj)
        except Exception:
            try:
                res = dumps(obj)
                open('errors.log', 'a').write(res)
            except Exception:
                pass
