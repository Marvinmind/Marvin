class MessageCreator():
	def __init__(self,sender):
		self.sender = str(sender)
	def buildMessage(self, in_text,sender):
		m = Message(in_text, sender)
		return m

class Message():
	def __init__(self, in_text, sender):
		self.body = in_text
		self.sender = sender

	def verify(self):
		return 'VERIFIED'