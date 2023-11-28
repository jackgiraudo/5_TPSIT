import socket
from time import sleep, time
import datetime
import random

#Sirena che setto a True quando è attiva
SIRENA = False

# Creazione di un socket IPv4 in modalità TCP per il client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specifica dell'indirizzo IP e della porta del server a cui il client si connetterà
server_address = ("192.168.56.1", 8000)

def main():
    global SIRENA
    
    # Connessione al server
    s.connect(server_address)
    
    while True:
        sleep(10)

        #livello acqua (nella realtà sara preso da un sensore)
        livello_int = random.randint(0, 9) 
        livello_float = float(livello_int)

        ora_giorno = str(datetime.datetime.now())
        print(ora_giorno)
        # Richiesta di input dall'utente
        str_send = str(livello_float)

        # Codifica della stringa in formato binario (bytes)
        str_bin = str_send.encode()
        str_info = ora_giorno.encode()

        # Invio della stringa codificata al server
        s.sendall(str_bin)
        s.sendall(str_info)

        # Ricezione della risposta dal server (con una dimensione massima di 4096 byte)
        str_received = s.recv(4096).decode()
        print(str_received)

        #condizioni di stampa
        if str_received == "1":
            SIRENA == True
            print("STATO DI ALLARME")
        else:
            SIRENA = False
            

if __name__ == "__main__":
    main()