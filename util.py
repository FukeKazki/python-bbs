from dataclasses import dataclass
from socket import (
	socket,
	AF_INET,
	SOCK_STREAM,
)


@dataclass
class Message:
	id: str
	time: str
	handle_name: str
	content: str
	password: str


class Socket:
	sock = None
	sock_c = None
	BUF_SIZE = 1024
	state = 'client'

	def is_client(self):
		return self.state == 'client'

	def __init__(self, state):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.state = state

	def __del__(self):
		self.sock.close()

	def close_c(self):
		if not self.is_client():
			self.sock_c.close()

	def listen(self):
		self.sock.listen()

	def bind(self, address: tuple):
		if not self.is_client():
			self.sock.bind(address)

	def connect(self, address: tuple):
		self.sock.connect(address)

	def accept(self):
		if not self.is_client():
			self.sock_c, _ = self.sock.accept()

	def recv(self) -> str:
		if self.is_client():
			data = self.sock.recv(self.BUF_SIZE)
		else:
			data = self.sock_c.recv(self.BUF_SIZE)

		return data.decode('UTF-8')

	def send(self, message: str):
		data = message.encode('UTF-8')

		if self.is_client():
			self.sock.sendall(data)
		else:
			self.sock_c.sendall(data)
