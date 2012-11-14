from datetime import datetime
import email
from itertools import izip
from bson.son import SON

class EmailDocument(SON):
    def __init__(self, raw_email):
        self['Created'] = datetime.now()
        self._parse_email(raw_email)


    def _parse_email(self, input):
        message = email.message_from_string(input[1])

        # This part should be refactored using RegEx to doesn't count on order.
        ids = input[0].replace('(', '').split()
        raw = self._convert_email_to_dictionary(message)

        self['X-GM-THRID'] = ids[2]
        self['X-GM-MSGID'] = ids[4]
        self['UID'] = ids[6]

        self['From'] = raw['headers']['From']
        if 'To' in raw['headers']:
            self['To'] = raw['headers']['To']
        if 'CC' in raw['headers']:
            self['CC'] = raw['headers']['CC']

        self['Date'] = raw['headers']['Date']
        self['Subject'] = raw['headers']['Subject']

        if 'Message-ID' in raw['headers']:
            self['Message-ID'] = raw['headers']['Message-ID']
        elif 'Message-Id' in raw['headers']:
            self['Message-ID'] = raw['headers']['Message-Id']
        if 'In-Reply-To' in raw['headers']:
            self['In-Reply-To'] = raw['headers']['In-Reply-To']
        if 'References' in raw['headers']:
            self['References'] = raw['headers']['References']
        if 'List-ID' in raw['headers']:
            self['List-ID'] = raw['headers']['List-ID']

        self['RAW'] = raw
        # DEBUG
        del self['RAW']['payload']


    def _convert_email_to_dictionary(self, email):
        dictEmail = email.__dict__

        # We can remove not wanted fields here.

        dictEmail['headers'] = {}
        for key, value in dictEmail['_headers']:
            dictEmail['headers'][key] = value
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
