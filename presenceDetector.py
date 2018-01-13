# GrovePi + Grove Ultrasonic Ranger
import time
from grovepi import *
import threading
import socket

class EntranceUltrasonic(threading.Thread):

    def __init__(self,host,port):
        threading.Thread.__init__(self)
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

        lastValues = [50]*10
        print lastValues
        while True:
            try:
                time.sleep(1)
                print lastValues
                lastValues.append(ultrasonicRead(self.ultrasonic_ranger))
                if(len(lastValues) > 10):
                    lastValues = lastValues[1:]
                if self.isHomeFunction(lastValues):
                    print "Keys are in place !"
                    if not(self.isHome):
                        self.performAction("isHome")
                        self.isHome = True
                else:
                    print "Keys aren't in place !"
                    if self.isHome:
                        self.performAction("isNotHome")
                        self.isHome = False
            except KeyboardInterrupt:
                break
            except IOError:
                print "Error"

port = int(raw_input("Entrez le port d'ecoute : "))
host = raw_input("Entrez l'hote' : ")
ultrasonic = EntranceUltrasonic(host,port);
ultrasonic.start()
