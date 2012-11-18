from bson.son import SON
import email
from email import utils
from datetime import datetime


class EmailDocument(SON):
    def __init__(self, raw_email):
        metadata = raw_email[0].replace('(', '').split()

        # X-GM-MSGID as _id
        self['_created'] = datetime.now()

        self['X-GM-THRID'] = metadata[2]
        self['X-GM-MSGID'] = metadata[4]
        self['UID'] = metadata[6]

        msg = email.message_from_string(raw_email[1])

        if msg.has_key('Message-ID'):
            self['Message-ID'] = msg.get('Message-ID')
        elif msg.has_key('Message-Id'):
            self['Message-Id'] = msg.get('Message-Id')
        self['In-Reply-To'] = msg.get_all('In-Reply-To')
        self['References'] = msg.get_all('References')
        self['List-ID'] = msg.get('List-ID')

        self['From'] = utils.parseaddr(msg.get('From'))
        self['To'] = map(utils.parseaddr, msg.get_all('To'))
        if msg.has_key('Cc'):
            self['Cc'] = map(utils.parseaddr, msg.get_all('Cc'))

        self['Date'] = self._convert_string_to_date(msg.get('Date'))
        self['Subject'] = self.decode_text(msg.get('Subject'), msg)
        self['Body'] = self.get_body_from_email(msg)

        self['Raw'] = raw_email[1]


    def _convert_email_string_to_utf8(self, input):
        return utils.unquote(input)\
                    .decode("ISO-8859-1")\
                    .encode("utf8")


    def _convert_string_to_date(self, input):
        return datetime.fromtimestamp(utils.mktime_tz(utils.parsedate_tz(input)))


    def get_charsets(self, msg):
        charsets = set({})
        for c in msg.get_charsets():
            if c is not None:
                charsets.update([c])
        return charsets


    def handle_error(self, errmsg, emailmsg, cs):
        print()
        print(errmsg)
        print("This error occurred while decoding with ",cs," charset.")
        print("These charsets were found in the one email.",self.get_charsets(emailmsg))
        print("This is the subject:",emailmsg['subject'])
        print("This is the sender:",emailmsg['From'])


    def get_body_from_email(self, msg):
        body = None
        #Walk through the parts of the email to find the text body.
        if msg.is_multipart():
            for part in msg.walk():

                # If part is multipart, walk through the subparts.
                if part.is_multipart():

                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            # Get the subpart payload (i.e the message body)
                            body = subpart.get_payload(decode=True)
                            #charset = subpart.get_charset()

                # Part isn't multipart so get the email body
                elif part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    #charset = part.get_charset()

        # If this isn't a multi-part message then get the payload (i.e the message body)
        elif msg.get_content_type() == 'text/plain':
            body = msg.get_payload(decode=True)

        body = self.decode_text(body, msg)
        return body


    def decode_text(self, text, message):
        # No checking done to match the charset with the correct part.
        for charset in self.get_charsets(message):
            try:
                text = text.decode(charset)
            except UnicodeEncodeError:
                self.handle_error("UnicodeEncodeError: encountered.", message, charset)
            except UnicodeDecodeError:
                self.handle_error("UnicodeDecodeError: encountered.", message, charset)
            except AttributeError:
                self.handle_error("AttributeError: encountered", message, charset)

        return text