import AlphaBot
import socket
import time
import RPi.GPIO as GPIO
from threading import Thread, Lock

mutex = Lock()

DR = 16
DL = 19

MY_ADDRESS = ("0.0.0.0", 8000)
BUFF_SIZE = 4096

MOVING = False

class Sensor(Thread):
    def __init__(self, connection, address):
        
        #inizializzo classe thread
        Thread.__init__(self)

        #inizializzo la connection e l'address
        self.connection = connection
        self.address = address

        #sensori
        self.DL = DL
        self.DR = DR

        #libreria
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

    def run(self):
        global MOVING
        print('running')
        self.warning = False
        while True:
            if MOVING == True:
                self.warning = False
                self.connection.sendall(f"{GPIO.input(self.DL)}, {GPIO.input(self.DR)}".encode('utf-8'))
                time.sleep(0.5)
            else:
                if self.warning == False:
                    self.connection.sendall(f'stop'.encode('utf-8'))
                    self.warning = True




def main():
    global MOVING
    piero = AlphaBot.AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    connection, address = s.accept()

    sensor = Sensor(connection, address)
    sensor.start()

    dict = {'F': piero.forward, 'B': piero.backward, 'L': piero.left, 'R':piero.right}
    while True:
        try:
            text_received = connection.recv(BUFF_SIZE).decode('utf-8')
            print(text_received)
            command, dly = text_received.split(";")
            if command != '' and command in dict:
                mutex.acquire()
                MOVING = True
                mutex.release()
                dict[command]()
                time.sleep(int(dly))

                piero.stop()
                mutex.acquire()
                MOVING = False
                mutex.release()

        except KeyboardInterrupt:
            s.close()
            GPIO.cleanup()
            sensor.join()
            connection.close()


if __name__ == '__main__':
    main()