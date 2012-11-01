import imaplib
import email

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
        mailBox.list()
        mailBox.select(self.config.IMAP['Folder'])
        return mailBox

    def retrieveEmails(self, mailBox):
        result, data = mailBox.uid('search', None, self.config.IMAP['Search'])
        latest_email_uid = data[0].split()[-1]
        result, data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')
        uid = data[0][0]
        raw_email = data[0][1]
        mail = email.message_from_string(raw_email)

        cleanEmail = self.convertEmailToDictionary(mail)
        cleanEmail['_id'] = uid
        self.dao.save(cleanEmail)

    def convertEmailToDictionary(self, email):
        cleanEmail = email.__dict__

        cleanEmail['headers'] = cleanEmail['_headers']
        del cleanEmail['_headers']
        cleanEmail['payload'] = cleanEmail['_payload']
        del cleanEmail['_payload']
        cleanEmail['charset'] = cleanEmail['_charset']
        del cleanEmail['_charset']
        cleanEmail['default_type'] = cleanEmail['_default_type']
        del cleanEmail['_default_type']
        cleanEmail['unixfrom'] = cleanEmail['_unixfrom']
        del cleanEmail['_unixfrom']

        if not isinstance(cleanEmail['payload'], str):
            for payload in cleanEmail['payload']:
                payload = self.convertEmailToDictionary(payload)

        return cleanEmail
