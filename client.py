import socket, select, errno, sys

IP = "127.0.0.1";
PORT = 1234;
HEADER_LENGTH = 1024;
LOGOUT = "logout";
my_username = input("Username: ");

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client_socket.connect((IP, PORT));
client_socket.setblocking(False);

username = my_username.encode("utf-8");
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8');
client_socket.send(username_header + username);


while True:
	message = input(f"{my_username}@client > ");
	# message = "";				
	
	if message:
		message = message.encode('utf-8');
		message_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8");
		client_socket.send(message_header + message);
	try:
		while True:
			#receive things here
			username_header = client_socket.recv(HEADER_LENGTH);
			if not len(username_header):
				print("Connection closed by the server");
				sys.exit();

			username_length = int(username_header.decode("utf-8").strip());
			username = client_socket.recv(username_length).decode("utf-8");

			message_header = client_socket.recv(HEADER_LENGTH);
			message = client_socket.recv(HEADER_LENGTH).decode("utf-8");

			print(f"{username}@client > {message}");
			if message == LOGOUT:
				client_socket.close();	
				sys.exit();

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print(f"Reading error {str(e)}");
			sys.exit();
		continue;

	except Exception as e:
		print(f"General error {str(e)}");
		sys.exit();