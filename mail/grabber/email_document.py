import email
from bson.son import SON

class EmailDocument(SON):
    def __init__(self, raw_email):
        self._parse_email(raw_email)


    def _parse_email(self, input):
        message = email.message_from_string(input[1])

        # This part should be refactored using RegEx to doesn't count on order.
        ids = input[0].replace('(', '').split()

        # X-GM-MSGID to be the database _id
        self['_id'] = ids[4]
        # X-GM-THRID
        self[ids[1]] = ids[2]
        # X-GM-MSGID
        self[ids[3]] = ids[4]
        # UID
        self[ids[5]] = ids[6]

        self['content'] = self._convert_email_to_dictionary(message)


    def _convert_email_to_dictionary(self, email):
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
                dictEmail['payload'][i] = self._convert_email_to_dictionary(dictEmail['payload'][i])

        return dictEmail
