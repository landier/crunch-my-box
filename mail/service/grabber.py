import imaplib
import email
from datetime import datetime

BATCH_SIZE = 10

class Grabber(object):
    def __init__(self, config, dao):
        self.config = config
        self.dao = dao


    def run(self):
        mailBox = self.connectEmailAccount()
        self.retrieveEmails(mailBox)


    def connectEmailAccount(self):
        mailBox = imaplib.IMAP4_SSL(self.config.IMAP['Host'])
        mailBox.login(self.config.IMAP['Username'], self.config.IMAP['Password'])
        #pprint(mailBox.list())
        mailBox.select(self.config.IMAP['Folder'])
        return mailBox


    def retrieveEmails(self, mailBox):
        # Search in mailbox for matching emails.
        result, data = mailBox.uid('search', None, self.config.IMAP['Search'])
        if result != 'OK':
            print('Issue while searching: ' + result)
            exit(1)

        uids = data[0].split(' ')
        nbUids = str(len(uids))
        print(str(datetime.now()) + ' - Search: ' + self.config.IMAP['Search'] + ' - Results: ' + nbUids)
        uidSearchResult = list(self.chunks(uids, BATCH_SIZE))

        # Fetch found emails by 10 size batch then save them in DB.
        for n in range(0, len(uidSearchResult)):
            uidBatch = ','.join(uidSearchResult[n])
            result, data = mailBox.uid('fetch', uidBatch, self.config.IMAP['DataFormat'])
            if result != 'OK':
                print('Issue while fetching: ' + result)
                exit(1)

            print(str(datetime.now()) + ' - Fetching: ' + str(len(uidSearchResult[n]) + n * BATCH_SIZE) + '/' + nbUids)

            for i in range(0, len(data), 2):
                mail = self.parseEmail(data[i])
                self.dao.save(mail)


    def parseEmail(self, input):
        raw_message = email.message_from_string(input[1])

        # This part should be refactored using RegEx to doesn't count on order.
        ids = input[0].replace('(', '').split()
        setattr(raw_message, '_id', ids[4]) # X-GM-MSGID to be the CouchDB _id
        setattr(raw_message, ids[1], ids[2]) # X-GM-THRID
        setattr(raw_message, ids[3], ids[4]) # X-GM-MSGID
        setattr(raw_message, ids[5], ids[6]) # UID

        return self.convertEmailToDictionary(raw_message)


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


    def chunks(self, l, n):
        """ Yield successive n-sized chunks from given list. """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
