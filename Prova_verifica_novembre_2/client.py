import socket
from threading import Lock
from tkinter import E

mutex = Lock()

# Creazione di un socket IPv4 in modalità TCP per il client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specifica dell'indirizzo IP e della porta del server a cui il client si connetterà
server_address = ("192.168.56.1", 8000)

def main():
    # Connessione al server
    s.connect(server_address)

    while True:
        try:
            # Ricezione della risposta dal server (con una dimensione massima di 4096 byte)
            str_received = s.recv(4096).decode()

            # Stampare la risposta ricevuta dal server
            print(str_received)

            if str_received != "exit":
                ris = str(eval(str_received))
                print(ris)
                str_bin = ris.encode()
                s.sendall(str_bin)
            else:
                s.close()

        except:
            print("Sintassi non valida")

if __name__ == "__main__":
    main()