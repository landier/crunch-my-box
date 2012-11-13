import imaplib
import email
from datetime import datetime
from email_document import EmailDocument

class Grabber(object):
    BATCH_SIZE = 50
    DATA_FORMAT = '(UID X-GM-MSGID X-GM-THRID RFC822)'


    def __init__(self, config, dao):
        self.config = config
        self.dao = dao


    def run(self):
        mailBox = self.connectToEmailAccount(self.config.IMAP['Host'],
                                                  self.config.IMAP['Username'],
                                                  self.config.IMAP['Password'],
                                                  self.config.IMAP['Folder'])
        self.retrieveEmails(mailBox, self.config.IMAP['Search'])


    def connectToEmailAccount(self, host, username, password, folder):
        mailBox = imaplib.IMAP4_SSL(host)
        mailBox.login(username, password)
        mailBox.select(folder)
        return mailBox


    def retrieveEmails(self, mailBox, search):
        # Search in mailbox for matching emails.
        result, data = mailBox.uid('search', None, search)
        if result != 'OK':
            print('Issue while searching: ' + result)
            exit(1)

        uidEmailList = data[0].split(' ')
        nbOfEmails = str(len(uidEmailList))
        print(str(datetime.now()) + ' - Search: ' + search + ' - Results: ' + nbOfEmails)
        uidFetchLists = self.splitListToNLists(uidEmailList, Grabber.BATCH_SIZE)

        # Fetch found emails by 10 size batch then save them in DB.
        for n in range(0, len(uidFetchLists)):
            uidBatch = ','.join(uidFetchLists[n])
            result, data = mailBox.uid('fetch', uidBatch, Grabber.DATA_FORMAT)
            if result != 'OK':
                print('Issue while fetching: ' + result)
                exit(1)

            print(str(datetime.now()) + ' - Fetching: ' + str(len(uidFetchLists[n]) + n * Grabber.BATCH_SIZE) + '/' + nbOfEmails)

            for i in range(0, len(data), 2):
                emailDoc = EmailDocument(data[i])
                self.dao.save(emailDoc)

    def splitListToNLists(self, list, rowSize):
        """ Yield successive n-sized chunks from given list. """
        resultList = []
        for i in xrange(0, len(list), rowSize):
            resultList.append(list[i:i+rowSize])

        return resultList
