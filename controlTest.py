import getpass
import sys

import stem
import stem.connection

from stem.control import Controller

if __name__ == '__main__':
	controller = Controller.from_port()
	controller.authenticate(password='muenster')
	desc = controller.get_hidden_service_descriptor('ogok5j2jcrh2a5hg.onion')
	print(desc)