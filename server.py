import socket, select

# ------------------------------------------------------------------------------ #
# -------------------------------- Constants Socket ---------------------------- #
IP = "127.0.0.1";
PORT = 1234;
HEADER_LENGTH = 1024;
CMD_DELIMITOR = " ";
# ------------------------------------------------------------------------------ #


# -------------------------------- Constants command--------------------------- #
CMD_QUIT = "QUIT";
MSG_QUIT = "Leaved"
CMD_MSG = "MSG";

CMD_NICK = "NICK";
CMD_KILL = "KILL";
MSG_KIL = "Stopped"
# ------------------------------------------------------------------------------ #
# -------------------------------- Init ---------------------------------------- #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
s.bind((IP, PORT));
s.listen(HEADER_LENGTH);
s_list = [s];
clients = {};

# ------------------------------------------------------------------------------ #


def receive_message(client_socket):
	try:
		message_hedaer = client_socket.recv(HEADER_LENGTH);
		if not len(message_hedaer):
			return False;
		message_length = int(message_hedaer.decode("utf-8").strip());
		return {"header": message_hedaer, "data": client_socket.recv(HEADER_LENGTH)};
	except:
		return False;


while True:
	read_sockets, _, exception_sockets = select.select(s_list, [], s_list);
	for notified_socket in read_sockets:
		if notified_socket == s:
			client_socket, client_address = s.accept();
			user = receive_message(client_socket);
			if user is False:
				continue;
			s_list.append(client_socket);
			clients[client_socket] = user;
			print(f"Accepted new connection {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}");
		else:
			message = receive_message(notified_socket);
			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}");
				s_list.remove(notified_socket);
				del clients[notified_socket];
				continue;
			user = clients[notified_socket];
			data = message['data'].decode('utf-8');
			cmd_line = data.split(CMD_DELIMITOR);
			type_cmd = cmd_line[0];
			msg = "";
			if type_cmd == CMD_QUIT :
				msg = MSG_QUIT;
				if len(cmd_line) == 2 :
					msg += " by saying : " + cmd_line[1];
				print(f"Received message from {user['data'].decode('utf-8')} : {data}");
				for c_socket in clients:
					if c_socket != notified_socket:
						c_socket.send(user['header']+user['data']+message['header']+msg.encode('utf-8'));

				client_socket.send(user['header']+user['data']+message['header']+"logout".encode('utf-8'));
				client_socket.close();
				s_list.remove(notified_socket);
				del clients[notified_socket];

			if type_cmd == CMD_MSG:
				if len(cmd_line) == 2 :
					msg = cmd_line[1];
					print(f"Received message from {user['data'].decode('utf-8')} : {data}");

				for c_socket in clients:
					if c_socket != notified_socket:
						c_socket.send(user['header']+user['data']+message['header']+msg.encode('utf-8'));

	for notified_socket in exception_sockets:
		s_list.remove(notified_socket);
		del clients[notified_socket];