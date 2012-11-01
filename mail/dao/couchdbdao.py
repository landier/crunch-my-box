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
        json = obj.__dict__
        json['headers'] = json['_headers']
        del json['_headers']
        json['payload'] = json['_payload']
        del json['_payload']
        json['charset'] = json['_charset']
        del json['_charset']
        json['default_type'] = json['_default_type']
        del json['_default_type']
        json['unixfrom'] = json['_unixfrom']
        del json['_unixfrom']
        self.db.save(json)
