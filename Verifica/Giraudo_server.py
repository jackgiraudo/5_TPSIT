from threading import Thread
import socket
import sqlite3 as sql

#percentuale: manda 4 --> 4 : valore * 100 

BUFF_SIZE = 4096

# Creazione di un socket IPv4 in modalità TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specifica dell'indirizzo IP e della porta del server
my_address = ("0.0.0.0", 8000)

# Associazione del socket all'indirizzo specificato
s.bind(my_address)

# Classe che estende Thread per gestire singoli client
class Client_thread(Thread):
    def __init__(self, connection, fiume, localita):
        Thread.__init__(self)
        self.connection = connection
        self.fiume = fiume
        self.localita = localita

    # Metodo che viene eseguito quando il thread viene avviato
    def run(self):
        #print(self.localita, self.fiume) debug

        while True:
            str_bin = self.connection.recv(BUFF_SIZE) #stringa del livello
            str_info_bin = self.connection.recv(BUFF_SIZE)
            str_info = str_info_bin.decode()
            
            #ricavo il giorno e l'ora splittando sullo spazio che hanno in mezzo
            giorno, ora = str_info.split(" ")
            
            livello_recivuto_str = str_bin.decode("utf-8")
            livello_ricevuto_float = float(livello_recivuto_str)
            print(f"Livello ricevuto : {livello_ricevuto_float} il giorno : {giorno} alle ore: {ora}")

            #connessione al db
            conSQL = sql.connect("fiumi.db")
            cur = conSQL.cursor()

            #mi ricavo il livello dal db
            research = cur.execute(f"SELECT l.livello from livelli l where l.fiume = '{self.fiume}' and l.localita = '{self.localita}'")
            livello_str = research.fetchall()[0][0]
            livello_float = float(livello_str)
            #chiudo db
            conSQL.close()

            #calcolo percentuale livello ricevuto
            perc = (livello_ricevuto_float / livello_float) * 100

            #casistiche dei livelli 
            if perc < 30:
                self.connection.sendall("Ricevuto".encode())
            elif perc >= 30 and perc < 70:
                print(f"PERICOLO IMMINENTE fiume {self.fiume}, localita {self.localita}")
                self.connection.sendall("Ricevuto, pericolo imminente".encode())
            elif perc >= 70:
                print(f"PERICOLO IN CORSO fiume {self.fiume}, localita {self.localita}")
                self.connection.sendall("1".encode())


            
# Funzione principale del server
def main():
    client_list = []  # Lista per memorizzare i thread dei singoli client
    count_client = 0

    #fiume e localià che mi ricavo dal db
    fiume = ""
    localita = ""

    try:
        while True:
            # Il server è in ascolto di nuove connessioni
            s.listen() 

            # Accettazione della connessione dal client 
            connessione, address = s.accept()
            count_client += 1

            #connessione al db
            #connessione al db
            conSQL = sql.connect("fiumi.db")
            cur = conSQL.cursor()

            #fiume dal db 
            research = cur.execute(f"SELECT l.fiume from livelli l where l.id_stazione = {count_client}")
            fiume = research.fetchall()[0][0]
            #print (fiume)

            #chiudo db
            conSQL.close()

            #connessione al db
            conSQL = sql.connect("fiumi.db")
            cur = conSQL.cursor()

            #fiume dal db 
            research = cur.execute(f"SELECT l.localita from livelli l where l.id_stazione = {count_client}")
            localita = research.fetchall()[0][0]
            #print (localita)

            #chiudo db
            conSQL.close()

            # Creazione di un nuovo thread per il client  
            client = Client_thread(connessione, fiume, localita)  

            # Aggiunta del thread alla lista
            client_list.append(client)  

            # Avvio del thread per gestire il client
            client.start() 

    except KeyboardInterrupt:
        print("Chiusura del server...")

        # Chiusura di tutte le connessioni dei client
        for client in client_list:
            client.join()  # Attendere che ciascun thread del client termini
            print(f"Thread del client {client.getName()} terminato.")

        s.close()  # Chiusura del socket del server

if __name__ == "__main__":
    main()