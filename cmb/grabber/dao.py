from datetime import datetime
from pymongo import Connection
from json import dumps


class DAO(object):
    def __init__(self, config):
        self._connect_to_database(config.DB['Host'], config.DB['Port'], config.DB['Name'], config.DB['Collection'])


    def _connect_to_database(self, host, port, name, collection):
        connection = Connection(host, int(port))
        self.collection = connection[name][collection]
        print(str(datetime.now()) + '- Connected to database: ' + host + ':' + port + '/' + name + '/' + collection)


    def save(self, obj):
        doc = self.collection.find_one({ 'X-GM-MSGID': obj['X-GM-MSGID'] })

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
