from couchdb.client import Server

class CouchDBDao(object):
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        server = Server(self.config.DB['Host'])
        try:
            self.db = server.create(self.config.DB['Name'])
        except Exception:
            self.db = server[self.config.DB['Name']]

    def save(self, obj):
        doc = self.db.get(obj['_id'])

        if doc is not None:
            obj['_rev'] = doc['_rev']

        self.db.save(obj)
