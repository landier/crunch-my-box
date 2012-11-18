def _convert_email_text_to_utf8(input):
    return input.decode("quopri")\
    .decode("ISO-8859-1")\
    .encode("utf8")

import rfc822
def _convert_string_to_date(input):
    return rfc822.parsedate(input)



text = '''\r\nPurchase Date: Oct 7, 2011\r\nUnit Price: =2436.49 USD\r\nQty: 1\r\nAmount: =2436.49 USD\r\nSubtotal: =2436.49 USD\r\nShipping and handling: =240.00 USD\r\nInsurance - not offered : ----\r\n----------------------------------------------------------------------\r\nTax: --\r\nTotal: =2436.49 USD\r\nPayment: =2436.49 USD\r\nPayment sent to: emailaddress=40gmail.com\r\n----------------------------------------------------------------------\r\n\r\nSincerely,\r\nPayPal\r\n=20\r\n----------------------------------------------------------------------\r\nHelp Center:=20\r\nhttps://www.paypal.com/us/cgi-bin/helpweb?cmd=3D_help\r\nSecurity Center:=20\r\nhttps://www.paypal.com/us/security\r\n\r\nThis email was sent by an automated system, so if you reply, nobody will =\r\nsee it. To get in touch with us, log in to your account and click =\r\n=22Contact Us=22 at the bottom of any page.\r\n\r\n'''
raw_data = text.decode("quopri") #replace =XX for the real characters
data = [map(str.strip, l.split(":")) for l in raw_data.splitlines() if ": " in l]
print data

date = _convert_string_to_date("Mon, 5 Nov 2012 16:54:27 +0100")
print date


