import json
from typing import Final
from util import Socket
import multiprocessing

LOG_FILE_PATH: Final = 'log.json'


def read_json(file_path: str) -> dict:
	with open(file_path, 'r') as file:
		return json.load(file)


def write_json(file_path: str, data: dict) -> None:
	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)


def remove_key(dictionary: dict, key: str) -> dict:
	dictionary.pop(key)
	return dictionary


def remove_dict(_list: list, dictionary: dict):
	new_list = []
	for dic in _list:
		if dic['password'] != dictionary['password']:
			new_list.append(dic)
	return new_list


def bbs(sock):
	data = sock.recv()
	data = json.loads(data)
	state = data['state']

	if state == 'read':
		log_file = read_json(LOG_FILE_PATH)
		log_messages = log_file['messages']
		messages = [remove_key(message, 'password') for message in log_messages]
		messages = json.dumps(messages)
		sock.send(messages)

	elif state == 'write':
		message = data['message']
		log_file = read_json(LOG_FILE_PATH)
		log_messages = log_file['messages']
		log_messages.append(message)
		write_json(LOG_FILE_PATH, {'messages': log_messages})

	elif state == 'delete':
		message = data['message']
		log_file = read_json(LOG_FILE_PATH)
		log_messages = log_file['messages']
		messages = remove_dict(log_messages, message)
		write_json(LOG_FILE_PATH, {'messages': messages})


# TODO 結果をクライアントに送信 (成功・失敗)
def main():
	sock = Socket('server')
	sock.bind(("", 50000))
	sock.listen()
	while True:
		sock.accept()
		p = multiprocessing.Process(target=bbs, args=(sock,))
		p.start()


if __name__ == '__main__':
	main()
