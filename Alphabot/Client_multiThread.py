import socket
from threading import Thread, Lock

mutex = Lock()

MOVING = False

class readSensor(Thread):
    def __init__(self, socket):

        #inizializzo classe thread
        Thread.__init__(self)

        #inizializzo la connection e l'address
        self.socket = socket

    def run(self):
        global MOVING
        while True:
            self.received = self.socket.recv(4096).decode('utf-8')
            print(self.received)
            mutex.acquire()
            if self.received != 'stop':
                MOVING = True
                #print(self.received)
            else:
                MOVING = False
            mutex.release()

def main():
    global  MOVING
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.1.131', 8000)
    s.connect(server_address)
    print('connesso')
    readThread = readSensor(s)
    readThread.start()

    while True:
        if MOVING == False:
            text = input('Inserisci comando:')
            text_b = text.encode()
            s.sendall(text_b)

if __name__ == '__main__':
    main()