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
        result, data = mailBox.uid('search', None, "ALL") # search and return uids instead
        latest_email_uid = data[0].split()[-1]
        result, data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')
        uid = data[0][0]
        raw_email = data[0][1]
        mail = email.message_from_string(raw_email)
        self.dao.save(uid, mail)
