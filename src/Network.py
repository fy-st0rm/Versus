import socket


class Network:
	def __init__(self, SERVER, PORT):
		self.SERVER = SERVER
		self.PORT = PORT
		self.BUFF_SIZE = 2048
		self.FORMAT = "utf-8"
		self.ADDR = (self.SERVER, self.PORT)

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		try:
			# Trying to connect to the server
			self.client.connect(self.ADDR)
			return pickle.loads(self.client.recv(self.BUFF_SIZE))
		except:
			pass