import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.131', 8000)
s.connect(server_address)
print('connesso')

while True:
    text = input('Inserisci comando:')
    text_b = text.encode()
    s.sendall(text_b)
    print(s.recv(4096).decode('utf-8'))