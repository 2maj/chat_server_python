import socket, sys, 

IP = "127.0.0.1";
PORT = 1210;
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind((IP, PORT));
s.listen(1);
clientsocket, address = s.accept();
print(f"Connection from {address} has been established!");
while True:
	# clientsocket.sendall(bytes("Welcome to the server !"));
	cmd = input("$ ");
	cmd = cmd.encode("utf-8");
	if cmd == b'quit':
		clientsocket.sendall(cmd);
		clientsocket.close();
		
	else:
		clientsocket.sendall(cmd);
		client_response = str(clientsocket.recv(1024), "utf-8");
		print(client_response);
s.close();	
sys.exit();