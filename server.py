from typing import Final, List
from util import Action, Log, Server, Response, State, Message
import multiprocessing

LOG_FILE_PATH: Final = 'log.json'


def remove_password(message: Message) -> Message:
	message.password = None
	return message


def delete_message(_list: List[Message], message: Message) -> List[Message]:
	return [m for m in _list if m.password != message.password]


def bbs(sock: Server):
	body = sock.recv_body()
	log = Log(LOG_FILE_PATH)

	if body.action == Action.READ.value:
		log_messages = log.read_messages()
		messages = [remove_password(message) for message in log_messages]
		response = Response(
			state=State.SUCCESS.value,
			messages=messages
		)
		sock.send_response(response)

	elif body.action == Action.WRITE.value:
		message = Message(**body.message)
		log_messages = log.read_messages()
		log_messages.append(message)
		log.write_messages(log_messages)

		response = Response(
			state=State.SUCCESS.value
		)
		sock.send_response(response)

	elif body.action == Action.DELETE.value:
		message = Message(**body.message)
		log_messages = log.read_messages()
		messages = delete_message(log_messages, message)
		log.write_messages(messages)

		response = Response(
			state=State.SUCCESS.value
		)
		sock.send_response(response)


def main():
	sock = Server(("", 50000))
	while True:
		sock.accept()
		p = multiprocessing.Process(target=bbs, args=(sock,))
		p.start()


if __name__ == '__main__':
	main()
