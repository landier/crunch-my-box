from bson.son import SON
from pymongo.connection import Connection
from util.configuration import Configuration

class Test(SON):
    def __init__(self):
        self['_id'] = 'nla'
        self['a'] = 1
        self['b'] = 2
        self['c'] = ('tata', 'toto', 'titi')


test = Test()
print(test)


config = Configuration('../../../settings.ini')

connection = Connection(config.DB['Host'], int(config.DB['Port']))
collection = connection['mail']['emails']
collection.save(test)


