# GrovePi + Grove Ultrasonic Ranger
import time
from grovepi import *
import threading
import socket

class EntranceUltrasonic(threading.Thread):

    def __init__(self,host,port):
        threading.Thread.__init__(self)
        # Connect the Grove LED to digital port D3
        self.led = 3
        # Connect the Grove Ultrasonic Ranger to digital port D4
        self.ultrasonic_ranger = 4

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.s.connect((self.host, self.port))

    def performAction(self,action):
        self.s.send(action)
        r = self.s.recv(9999999)
        return r

    def isHomeFunction(self,data):
        nbFalse = 0
        for value in data:
            if value > 15:
                nbFalse = nbFalse + 1
                if nbFalse > 5:
                        return False
        return True

    def run(self):
        self.isHome = False
        self.performAction("isNotHome")
        pinMode(self.led,"OUTPUT")

        lastValues = [50]*10
        print lastValues
        digitalWrite(self.led,0)
        while True:
            try:
                time.sleep(1)
                print lastValues
                lastValues.append(ultrasonicRead(self.ultrasonic_ranger))
                if(len(lastValues) > 10):
                    lastValues = lastValues[1:]
                # Read distance value from Ultrasonic
                if self.isHomeFunction(lastValues):
                    print "Keys are in place !"
                    if not(self.isHome):
                        digitalWrite(self.led,1)
                        self.performAction("isHome")
                        self.isHome = True
                else:
                    print "Keys aren't in place !"
                    if self.isHome:
                        digitalWrite(self.led,0)
                        self.performAction("isNotHome")
                        self.isHome = False
            except KeyboardInterrupt:   # Turn LED off before stopping
                digitalWrite(self.led,0)
                break
            except IOError:
                print "Error"

port = int(raw_input("Entrez le port d'ecoute : "))
host = raw_input("Entrez l'hote' : ")
host = "192.168.1.81"
ultrasonic = EntranceUltrasonic(host,port);
ultrasonic.start()
