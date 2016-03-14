from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from stem.control import Controller

import hashlib, base64

class Message():
	def setSender(self,sender):
		self.sender = sender
	def setBody(self, message):
		self.body = message
	def getBody():
		return self.body
	def sign(self, privKey):
		with open(privKey, 'r') as keyfile:
			key = RSA.importKey(keyfile.read())
			hash = MD5.new(self.body).digest()
			signature = key.sign(hash,'')
			self.signature = signature
	def checkSignature(self):
		key = RSA.importKey(self.pubkey)
		status = key.verify(MD5.new(self.body).digest(), self.signature)
		print(base64.b32encode(hashlib.sha1(key.exportKey(format='DER')).digest()[:10]).lower())
		return status

if __name__== '__main__':
	location = '/var/lib/tor/'
	m = Message()
	m.setBody('hello world!')
	m.sign(location)
	print(m.signature)