from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import hashlib,  base64

class MessageCreator():
	def __init__(self,location):
		self.SERVICE_LOCATION = location
		with open(self.SERVICE_LOCATION+'/hostname','r') as f:
			self.sender = f.read().split('.')[0]
		with open(self.SERVICE_LOCATION+'/private_key','r') as k:
			self.key = RSA.importKey(k.read())
	def buildMessage(self, in_text):
		m = Message(in_text, self.key, self.sender)
		return m

class Message():
	def __init__(self, in_text, key, sender):
		self.body = in_text
		self.sender = sender
		hash = MD5.new(self.body.encode('utf-8')).digest()
		self.signature = key.sign(hash,'')
		self.pubkey = key.publickey().exportKey(format='PEM')
	
	def verify(self):
		key = RSA.importKey(self.pubkey)
		sigStatus = key.verify(MD5.new(self.body.encode('utf-8')).digest(), self.signature)
		calcID = base64.b32encode(hashlib.sha1(key.exportKey(format='DER')[22:]).digest()[:10]).lower().decode('ascii')
		print(calcID)
		if (calcID == self.sender) and sigStatus:
			return 'VERIFIED'
		else:
			return 'NOT VERIFIED'

class MessageCreatorSimple():
	def __init__(self,sender):
		self.sender = sender
	def buildMessage(self, in_text,sender):
		m = Message(in_text, sender)

class Message():
	def __init__(self, in_text, sender):
		self.body = in_text
		self.sender = sender

	def verify(self):
		return 'VERIFIED'

if __name__== '__main__':
	location = '/var/lib/tor/other_hidden_service'
	gen = MessageCreator(location)
	m = gen.buildMessage('hello world!')

	print(m.verify())

	
	