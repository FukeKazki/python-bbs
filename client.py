from util import Socket, Message
from uuid import uuid4
from datetime import datetime
from hashlib import sha256
from getpass import getpass
import json
from dataclasses import asdict


# TODO 送信結果を表示 (成功・失敗)


def main():
	state = input('何をしますか?\nwrite\nread\ndelete\n')
	sock = Socket('client')
	sock.connect(("localhost", 50000))

	if state == 'write':
		identify = str(uuid4())[:6]
		time = str(datetime.now())
		handle_name = input('handle_name: ')
		content = input('content: ')
		password = getpass('password: ')
		password = sha256(password.encode() + identify.encode()).hexdigest()

		message = Message(identify, time, handle_name, content, password)
		message = asdict(message)
		data = {
			'state': state,
			'message': message
		}
		json_data = json.dumps(data)
		sock.send(json_data)
	elif state == 'read':
		data = {
			'state': state
		}
		data = json.dumps(data)
		sock.send(data)
		data = sock.recv()
		data = json.loads(data)
		for message in data:
			print('--------------------')
			print(f"ID: {message['id']}")
			print(f"TIME: {message['time']}")
			print(f"HANDLE NAME: {message['handle_name']}")
			print(f"CONTENT: {message['content']}")
		pass
	elif state == 'delete':
		identify = input('id: ')
		password = getpass('password: ')
		password = sha256(password.encode() + identify.encode()).hexdigest()
		data = {
			'state': state,
			'message': {
				'id': identify,
				'password': password
			}
		}
		data = json.dumps(data)
		sock.send(data)
	else:
		pass


if __name__ == '__main__':
	main()
