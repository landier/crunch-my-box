from couchdb.client import Server

class CouchDB(self):
    def connect(self):
        server = Server('http://localhost:5984')
        print(server)
        try:
            db = server.create('emails')
        except Exception:
            db = server['emails']
