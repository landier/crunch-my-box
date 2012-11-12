from datetime import datetime
from pymongo import Connection
from json import dumps

class DAO(object):
    def __init__(self, config):
        self.connectToDabase(config.DB['Host'], config.DB['Port'], config.DB['Name'], config.DB['Collection'])

    def connectToDabase(self, host, port, name, collection):
        connection = Connection(host, int(port))
        self.collection = connection[name][collection]
        print(str(datetime.now()) + '- Connected to database: ' + host + ':' + port + '/' + name + '/' + collection)

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
