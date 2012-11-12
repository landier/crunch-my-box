import email
from bson.son import SON

class Message(SON):
    def __init__(self, raw_email):
        self.parseEmail(raw_email)


    def parseEmail(self, input):
        self.email = email.message_from_string(input[1])

        # This part should be refactored using RegEx to doesn't count on order.
        ids = input[0].replace('(', '').split()
        self['_id'] = ids[4] # X-GM-MSGID to be the CouchDB _id
        self[ids[1]] = ids[2] # X-GM-THRID
        self[ids[3]] = ids[4] # X-GM-MSGID
        self[ids[5]] = ids[6] # UID

        self['content'] = self.convertEmailToDictionary(self).items


    def convertEmailToDictionary(self, email):
        dictEmail = email.__dict__

        # We can remove not wanted fields here.
        dictEmail['headers'] = dictEmail['_headers']
        del dictEmail['_headers']
        dictEmail['payload'] = dictEmail['_payload']
        del dictEmail['_payload']
        dictEmail['charset'] = dictEmail['_charset']
        del dictEmail['_charset']
        dictEmail['default_type'] = dictEmail['_default_type']
        del dictEmail['_default_type']
        dictEmail['unixfrom'] = dictEmail['_unixfrom']
        del dictEmail['_unixfrom']

        # Convert recursively payloads (messages) in this email.
        if isinstance(dictEmail['payload'], list):
            for i in range(0, len(dictEmail['payload'])):
                dictEmail['payload'][i] = self.convertEmailToDictionary(dictEmail['payload'][i])

        return dictEmail
