import imaplib
from datetime import datetime
from email_document import EmailDocument

class Grabber(object):
    BATCH_SIZE = 50
    DATA_FORMAT = '(UID X-GM-MSGID X-GM-THRID RFC822)'


    def __init__(self, config, dao):
        self.config = config
        self.dao = dao


    def run(self):
        mailBox = self._connect_to_email_account(self.config.IMAP['Host'],
                                                  self.config.IMAP['Username'],
                                                  self.config.IMAP['Password'],
                                                  self.config.IMAP['Folder'])
        self._retrieve_emails(mailBox, self.config.IMAP['Search'])


    def _connect_to_email_account(self, host, username, password, folder):
        mailBox = imaplib.IMAP4_SSL(host)
        mailBox.login(username, password)
        mailBox.select(folder)
        return mailBox


    def _retrieve_emails(self, mailBox, search):
        # Search in mailbox for matching emails.
        result, data = mailBox.uid('search', None, search)

        if result != 'OK':
            print('Issue while searching: ' + result)
            exit(1)

        uidEmailList = data[0].split(' ')
        nbOfEmails = str(len(uidEmailList))
        print(str(datetime.now()) + ' - Search: ' + search + ' - Results: ' + nbOfEmails)

        uidFetchLists = self._split_list_to_list_array(uidEmailList, Grabber.BATCH_SIZE)

        # Fetch found emails by N size batch then save them in DB.
        for n in range(0, len(uidFetchLists)):
            uidBatchList = ','.join(uidFetchLists[n])
            result, data = mailBox.uid('fetch', uidBatchList, Grabber.DATA_FORMAT)

            if result != 'OK':
                print('Issue while fetching: ' + result)
                exit(1)

            print(str(datetime.now()) + ' - Fetching: ' + str(len(uidFetchLists[n]) + n * Grabber.BATCH_SIZE) + '/' + nbOfEmails)

            for i in range(0, len(data), 2):
                emailDoc = EmailDocument(data[i])
                self.dao.save(emailDoc)


    def _split_list_to_list_array(self, list, rowSize):
        resultList = []

        for i in xrange(0, len(list), rowSize):
            resultList.append(list[i:i+rowSize])

        return resultList
