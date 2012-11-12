class Message(object):
    def __init__(self, uid = None, subject = None):
        self.Uid = uid
        self.Sender = None
        self.Recipients = None
        self.Date = None
        self.Subject = subject
        self.Message = None

    def __repr__(self):
        return str(self.Uid) + ": " + self.Subject