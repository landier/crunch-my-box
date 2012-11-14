from datetime import datetime
import email
from bson.son import SON
from htmllib import HTMLParser
from formatter import AbstractFormatter, DumbWriter

class EmailDocument(SON):
    def __init__(self, raw_email):
        metadata, data = self._parse_email(raw_email)
        self._fill_fields(metadata, data)


    def _fill_fields(self, metadata, data):
        self['Created'] = datetime.now()

        self['X-GM-THRID'] = metadata[2]
        self['X-GM-MSGID'] = metadata[4]
        self['UID'] = metadata[6]

        self['From'] = data['headers']['From']
        if 'To' in data['headers']:
            self['To'] = data['headers']['To']
        if 'CC' in data['headers']:
            self['CC'] = data['headers']['CC']

        self['Date'] = email.utils.parsedate_tz(data['headers']['Date'])
        self['Subject'] = data['headers']['Subject']

        if 'Message-ID' in data['headers']:
            self['Message-ID'] = data['headers']['Message-ID']
        elif 'Message-Id' in data['headers']:
            self['Message-ID'] = data['headers']['Message-Id']
        if 'In-Reply-To' in data['headers']:
            self['In-Reply-To'] = data['headers']['In-Reply-To']
        if 'References' in data['headers']:
            self['References'] = data['headers']['References']
        if 'List-ID' in data['headers']:
            self['List-ID'] = data['headers']['List-ID']

        self['Message'] = data['payload']

        self['Raw'] = data


    def _parse_email(self, input):
        metadata = input[0].replace('(', '').split()

        message = email.message_from_string(input[1])
        data = self._convert_email_to_dictionary(message)

        return metadata, data


    def _convert_email_to_dictionary(self, email):
        dictEmail = email.__dict__

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

        del dictEmail['_unixfrom']
        del dictEmail['defects']
        del dictEmail['epilogue']
        del dictEmail['preamble']

        # Convert recursively payloads (messages) in this email.
        if isinstance(dictEmail['payload'], list):
            for i in range(0, len(dictEmail['payload'])):
                dictEmail['payload'][i] = self._convert_email_to_dictionary(dictEmail['payload'][i])

        return dictEmail
