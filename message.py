from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import hashlib,  base64

KEY_LOCATION = '/var/lib/tor/other_hidden_service/private_key'


class Message():
	def setSender(self,sender):
		self.sender = sender
	def setBody(self, message):
		self.body = message
	def getBody():
		return self.body
	def sign(self):
		with open(KEY_LOCATION, 'r') as keyfile:
			key = RSA.importKey(keyfile.read())
			hash = MD5.new(self.body.encode('utf-8')).digest()
			signature = key.sign(hash,'')
			self.signature = signature
			try:
				self.pubkey = key.publickey().exportKey(format='PEM')
			except Exception as e:
				print(e)
	def checkSignature(self):
		key = RSA.importKey(self.pubkey)
		sigStatus = key.verify(MD5.new(self.body.encode('utf-8')).digest(), self.signature)
		calcID = base64.b32encode(hashlib.sha1(key.exportKey(format='DER')[22:]).digest()[:10]).lower().decode('ascii')
		print(calcID)
		return (calcID == self.sender) and sigStatus
if __name__== '__main__':
#	location = '/var/lib/tor/other_hidden_service/private_key'
	m = Message()
	m.setBody('hello world!')
#	m.sign(location)

	
	