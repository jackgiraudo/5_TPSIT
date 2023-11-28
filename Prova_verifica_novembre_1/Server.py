import socket 
from threading import Thread, Lock
import sqlite3 as sql

MY_ADDRESS = ('0.0.0.0', 8000)
BUFF_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = MY_ADDRESS
s.bind(server_address)

class t(Thread):
    def __init__(self, connection):
        self.connection = connection
        Thread.__init__(self)

    def run(self):
        while True:
            print("ok")
            str_bin = self.connection.recv(BUFF_SIZE)
            str = str_bin.decode("utf-8")
            

            if str[0] == '0':
                conSQL = sql.connect("file.db")#connessione al db
                cur = conSQL.cursor()
                list = str.split(';') #split per ottenere le info da cercare
                list[1] = "'" + list[1] + "'"#aggiungole ' al nome file
                print(list[1])
                
                try:
                    research = cur.execute(f"SELECT * FROM files WHERE nome = {list[1]}")
                    db_info = research.fetchall()[0][0]
                except:#se il file nonviene trovato entra in except
                    db_info = "Non trovato"
                
                conSQL.close()
                #db_info_send = str(db_info)
                if db_info != "Non trovato":
                    db_info = "Trovato"

                self.connection.sendall(db_info.encode())
                print(db_info)

            if str[0] == '1':
                conSQL = sql.connect("file.db")#connessione al db
                cur = conSQL.cursor()
                list = str.split(';') #split per ottenere le info da cercare
                list[1] = "'" + list[1] + "'"#aggiungole ' al nome file
                print(list[1])
                
                try:
                    research = cur.execute(f"SELECT count(f.id_file) as frammenti From frammenti f, files ffwhere f.id_file = ff.id_file and ff.nome = {list[1]}")
                    db_info = research.fetchall()[0][0]
                    print(db_info)
                except:#se il file nonviene trovato entra in except
                    db_info = "Non trovato"
                
                conSQL.close()
                #db_info_send = str(db_info)
                if db_info != "Non trovato":
                    db_info = "Trovato"

                self.connection.sendall(db_info.encode())
                print(db_info)


def main():
    lista_threads = []
    db = sql.connect("file.db")
    cur = db.cursor()

    while True:
        s.listen()
        connection, address = s.accept()
        client = t(connection)
        client.start()
        lista_threads.append(client)
        
 
if __name__ == '__main__':
    main()