import json

class Contacts():
	def __init__(self,number):
		with open('contacts'+str(number)+'.json','r') as f:
			self.contacts = json.loads(f.read())

if __name__=='__main__':
	c = Contacts()
	for con in c.contacts:
		if 'name' in con:
			print(con['name'])

