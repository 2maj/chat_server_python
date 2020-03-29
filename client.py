import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((socket.gethostname(), 1234));

buff = 2;
char = s.recv(buff);
msg = char;

while True:
	char = s.recv(buff);
	msg = msg + char;
	if len(char) == 1:
		break;
print(msg.decode("utf-8"));