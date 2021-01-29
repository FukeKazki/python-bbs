from util import Message, Action, Client, Body, State
from getpass import getpass


def main():
	action = input('何をしますか?\n1: 読み込み\n2: 書き込み\n3: 削除\n')
	sock = Client(("localhost", 50000))

	if action == Action.WRITE.value:
		handle_name = input('handle_name: ')
		content = input('content: ')
		password = getpass('password: ')

		message = Message(
			handle_name=handle_name,
			content=content,
			password=password
		).encryption()

		body = Body(
			action=Action.WRITE.value,
			message=message
		)

		sock.send_body(body)

		response = sock.recv_response()

		if response.state == State.FAILED.value:
			print('書き込みに失敗しました。')
		else:
			print('書き込みに成功しました。')

	elif action == Action.READ.value:
		body = Body(
			action=Action.READ.value
		)

		sock.send_body(body)

		response = sock.recv_response()

		if response.state == State.FAILED.value:
			print('受信に失敗しました。')

		for message in response.messages:
			print('--------------------')
			print(f"ID: {message.id}")
			print(f"TIME: {message.time}")
			print(f"HANDLE NAME: {message.handle_name}")
			print(f"CONTENT: {message.content}")

	elif action == Action.DELETE.value:
		identify = input('id: ')
		password = getpass('password: ')

		message = Message(
			id=identify,
			password=password
		).encryption()
		body = Body(
			action=Action.DELETE.value,
			message=message
		)

		sock.send_body(body)
		response = sock.recv_response()

		if response.state == State.FAILED.value:
			print('IDもしくはPASSWORDが間違っています。')
		else:
			print('削除に成功しました。')

	else:
		pass


if __name__ == '__main__':
	main()
