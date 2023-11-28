import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("192.168.56.1", 8000)

def main():
    s.connect(server_address)

    while True:
        str_send = input("Inserire")
        str_bin = str_send.encode()
        s.sendall(str_bin)
        str_received = s.recv(4096).decode()
        print(str_received)

if __name__ == "__main__":
    main()