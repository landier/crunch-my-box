from dao.couchdbdao import CouchDBDao
from service.grabber import Grabber
from util.configuration import Configuration

def main():
    config = Configuration()
    couchdb_dao = CouchDBDao(config)
    grabber = Grabber(config, couchdb_dao)
    grabber.run()

main()
