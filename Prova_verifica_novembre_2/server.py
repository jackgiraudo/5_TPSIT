from threading import Thread, Lock
import socket
import sqlite3 as sql

mutex = Lock()

# Creazione di un socket IPv4 in modalità TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specifica dell'indirizzo IP e della porta del server
my_address = ("0.0.0.0", 8000)

# Associazione del socket all'indirizzo specificato
s.bind(my_address)

# Classe che estende Thread per gestire singoli client
class Client_thread(Thread):
    def __init__(self, connection, num, information):
        Thread.__init__(self)
        self.connection = connection
        self.num = num
        self.information = information

    # Metodo che viene eseguito quando il thread viene avviato
    def run(self):
        print(self.information)
        for key in self.information:
            print("cerco le chiavi")
            if self.information[key] == self.num:
                print("espresione")
                expression = key
                expression_bin = expression.encode('utf-8')
                self.connection.sendall(expression_bin)
                
                str_bin = self.connection.recv(4096)
                stringa = str_bin.decode("utf-8")
                print(f"Il risulatato dell'espressione {expression} del client {self.num} e : {stringa}")
        #self.connection.sendall("exit".encode())
        


# Funzione principale del server
def main():
    client_list = []  # Lista per memorizzare i thread dei singoli client
    count = 0

    information = {}
    #numero di client
    max = 0

    #connessione al db
    conSQL = sql.connect("operations.db")
    cur = conSQL.cursor() 

    #cerco il numero massimo di client così so quanti ce ne sono 
    research = cur.execute("SELECT max(o.client) from operations o")
    max = research.fetchall()[0][0]
    print (max)

    for c in range(1, max+1):
        #ricerco l'operazione
        research = cur.execute(f"SELECT count(o.operation) from operations o where o.client == {c}")
        n_operations = research.fetchall()[0][0]
        print (n_operations)

        for i in range(0, n_operations):
            research = cur.execute(f"SELECT o.operation from operations o where o.client == {c}")
            db_info = research.fetchall()[i][0]
            information[db_info] = c

    while True:
        # Il server è in ascolto di nuove connessioni
        s.listen() 

        # Accettazione della connessione dal client 
        connessione, address = s.accept()
        count += 1
        print(count)
        # Creazione di un nuovo thread per il client  
        client = Client_thread(connessione, count, information) 

        # Avvio del thread per gestire il client
        client.start()  
        print("ok")

        # Aggiunta del thread alla lista
        client_list.append(client)  
        

    s.close()  # Chiusura del socket del server

if __name__ == "__main__":
    main()