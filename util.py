from dataclasses import dataclass, asdict
from enum import Enum
from socket import socket, AF_INET, SOCK_STREAM
from hashlib import sha256
import json
from uuid import uuid4
from datetime import datetime
from typing import Final, List

BUF_SIZE: Final = 1024


class Action(Enum):
	READ = '1'
	WRITE = '2'
	DELETE = '3'


class State(Enum):
	SUCCESS = 'success'
	FAILED = 'failed'
	IDLE = 'idle'


@dataclass
class Message:
	id: str = str(uuid4())[:6]
	time: str = str(datetime.now())
	handle_name: str = None
	content: str = None
	password: str = None

	def encryption(self):
		plane_text = self.id + self.password
		self.password = sha256(plane_text.encode()).hexdigest()
		return self


@dataclass
class Response:
	state: str = State.IDLE.value
	messages: List[Message] = None


@dataclass
class Body:
	action: Action = Action.READ.value
	message: Message = None


@dataclass
class Log:
	file_path: str

	def read(self) -> dict:
		with open(self.file_path, 'r') as file:
			return json.load(file)

	def write(self, data: dict) -> None:
		with open(self.file_path, 'w') as file:
			json.dump(data, file, indent=4)

	def read_messages(self) -> List[Message]:
		data = self.read()
		data = [Message(**message) for message in data['messages']]
		return data

	def write_messages(self, data: List[Message]) -> None:
		data = [asdict(message) for message in data]
		self.write({'messages': data})


class Server:
	sock = None
	sock_c = None

	def __init__(self, address: tuple):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind(address)
		self.sock.listen()

	def __del__(self):
		self.sock.close()

	def accept(self):
		self.sock_c, _ = self.sock.accept()

	def recv(self) -> str:
		response = self.sock_c.recv(BUF_SIZE)
		return response.decode('UTF-8')

	def send(self, data: str):
		self.sock_c.sendall(data.encode('UTF-8'))

	def c_close(self):
		self.sock_c.close()

	def recv_body(self) -> Body:
		data = self.recv()
		data = json.loads(data)
		return Body(**data)

	def send_response(self, response: Response):
		data = asdict(response)
		data = json.dumps(data)
		self.send(data)


class Client:
	sock = None

	def __init__(self, address: tuple):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect(address)

	def __del__(self):
		self.sock.close()

	def recv(self) -> str:
		response = self.sock.recv(BUF_SIZE)
		return response.decode('UTF-8')

	def send(self, data: str) -> None:
		self.sock.sendall(data.encode('UTF-8'))

	def recv_response(self) -> Response:
		response = self.recv()
		data = json.loads(response)
		return Response(**data)

	def send_body(self, body: Body) -> None:
		data = asdict(body)
		data = json.dumps(data)
		self.send(data)
