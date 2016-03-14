from Crypto.PublicKey import RSA as RSAc
from Crypto.Hash import MD5
import StringIO
from M2Crypto import RSA as RSAm

class Message():
	def setSender(self,sender):
		self.sender = sender
	def setBody(self, message):
		self.body = message
	def getBody():
		return self.body
	def sign(self, privKey):
		with open(privKey, 'r') as keyfile:
			key = RSAc.importKey(keyfile.read())
			hash = MD5.new(self.body).digest()
			signature = key.sign(hash,'')
			self.signature = signature
			try:
				self.pubkey = key.publickey().exportKey(format='PEM')
			except Exception as e:
				print(e)
if __name__== '__main__':
	location = 'C:\Users\Martin\Tor\HiddenService\private_key'
	m = Message()
	m.setBody('hello world!')
	m.sign(location)
	out = StringIO.StringIO()
	k = RSAm.load_key(location)
	RSAm.save_pb_key(k)
	print('jo')
	
	