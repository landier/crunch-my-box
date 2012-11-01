import ConfigParser
from collections import defaultdict

class Configuration(object):
    def __init__(self, file = '../settings.ini'):
        error = False

        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.config.read(file)

        if not self.config.has_section('IMAP'):
            print "Missing IMAP section in settings file."
            error = True

        if not self.config.has_section('DB'):
            print "Missing DB section in settings file."
            error = True

        if error:
            exit(1)

    def __getattr__(self, item):
        try:
            itemList = self.config.items(str(item))
            dict = self.list_of_tuple_to_dictionary(itemList)
            return dict
        except ConfigParser.NoSectionError as ex:
            raise AttributeError(ex)
        except Exception as ex:
            raise AttributeError(ex)

    def list_of_tuple_to_dictionary(self, list_of_tuples):
        dictionary = defaultdict(str)
        for key, value in list_of_tuples:
            dictionary[key] = value
        return dictionary