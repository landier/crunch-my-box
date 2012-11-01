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
        mailBox.select("inbox")
        return mailBox

    def retrieveEmails(self, mailBox):
        result, data = mailBox.search(None, "ALL")
        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        result, data = mailBox.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        raw_email = data[0][1] # here's the body, which is raw text of the whole email
        print(raw_email)

        result, data = mailBox.uid('search', None, "ALL") # search and return uids instead
        latest_email_uid = data[0].split()[-1]
        result, data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email = self.parseEmail(raw_email)
        self.dao.save(email)

    def parseEmail(self, raw_email):
        email_message = email.message_from_string(raw_email)
        #print(email_message['To'])
        #print(email.utils.parseaddr(email_message['From'])) # for parsing "Yuji Tomita" <yuji@grovemade.com>
        #print(email_message.items()) # print all headers

        # note that if you want to get text content (body) and the email contains
        # multiple payloads (plaintext/ html), you must parse each message separately.
        # use something like the following: (taken from a stackoverflow post)
#        def get_first_text_block(self, email_message_instance):
#            maintype = email_message_instance.get_content_maintype()
#            if maintype == 'multipart':
#                for part in email_message_instance.get_payload():
#                    if part.get_content_maintype() == 'text':
#                        return part.get_payload()
#            elif maintype == 'text':
#                return email_message_instance.get_payload()
        return email_message
