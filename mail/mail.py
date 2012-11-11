from dao.couchdbdao import CouchDBDao
from dao.mongodbdao import MongoDBDao
from service.grabber import Grabber
from util.configuration import Configuration

def main():
    config = Configuration()

    #couchdb_dao = CouchDBDao(config)
    mongodb_dao = MongoDBDao(config)

    grabber = Grabber(config, mongodb_dao)
    grabber.run()

main()
