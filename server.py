#!/usr/bin/env python
# coding: utf-8
import os
import socket
import threading
import errno
import csv
import time
from tam import getNextTramTime
from sunset import getSunsetTime
from scheduler import Scheduler
from random import randint
from yeelight import Bulb

global isHome
global scheduler

scheduler = ""
isHome = False

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.bulb = Bulb("192.168.0.23",effect="smooth", duration=1000)
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self):
        print("Connection de %s %s" % (self.ip, self.port, ))
        while(True):
            try:
                r = self.clientsocket.recv(2048)
                if r:
                    print "Received : ", r
                    command = r.split("/")[0]
                    result = "UNKNOW_COMMAND"
                    if(command == "lightsOn"):
                        result = self.setLights(True)
                    elif(command == "lightsOff"):
                        result = self.setLights(False)
                    elif(command == "isHome"):
                        result = self.setHome(True)
			os.system("python script.py")
                    elif(command == "isNotHome"):
                        result = self.setHome(False)
                    elif(command == "say"):
                        try:
                            result = self.say(r.split("/")[1])
                        except IndexError:
                            print "Not enought arguments given !"
                            result = "NOT_ENOUGH_ARGUMENTS"
                    elif(command == "playSound"):
                        try:
                            result = self.playSound(r.split("/")[1])
                        except IndexError:
                            print "Not enought arguments given !"
                            result = "NOT_ENOUGH_ARGUMENTS"
                    elif(command == "setLightsTo"):
                        try:
                            result = self.setLightsTo(r.split("/")[1],r.split("/")[2],r.split("/")[3],r.split("/")[4])
                        except IndexError:
                            print "Not enought arguments given !"
                            result = "NOT_ENOUGH_ARGUMENTS"
                    elif(command == "setSceneTo"):
                        try:
                            result = self.setSceneTo(r.split("/")[1])
                        except IndexError:
                            print "Not enought arguments given !"
                            result = "NOT_ENOUGH_ARGUMENTS"
                    elif(command == "getNextTram"):
                        result = self.getNextTram()
                    elif(command == "getSunset"):
                        result = self.getSunset()
                    elif(command == "updateSunsetTask"):
                        scheduler.removeTask("lightsOn")
                        sunset = self.getSunset().split(" ")
                        task = [sunset[0],sunset[2],"lightsOn"]
                        print "Creation of task :",task
                        scheduler.addTask(task)
                        result = True

                    self.clientsocket.send(str(result))
                else:
                    self.clientsocket.close()
                    break
            except IOError, e:
                if e.errno == errno.EPIPE:
                    print "Client closed connection"
                    self.clientsocket.close()
                    break
                else:
                    print "WTF"
        print("Client déconnecté...")

    def getSunset(self):
        return getSunsetTime()

    def getNextTram(self):
        return getNextTramTime()

    def say(self,toSay):

        #TODO find a working tts library for python

        return True

    def playSound(self,soundPath):

        #TODO find a working sound playing library for python

        return True

    def setHome(self,state):
        print "Setting isHome to : ", state
        global isHome
        isHome = state
        return True

    def setLights(self,state):
        global isHome
        if isHome:
            if state:
                self.bulb.turn_on()
                print "Turning lights on ..."
                return True
            else:
                self.bulb.turn_off()
                print "Turning lights off ..."
                return True
        else:
            print "Not home"
            return False

    def setLightsTo(self,r,g,b,brightness):
        print "Setting lights to :", r,g,b,brightness
        self.bulb.set_brightness(brightness)
        self.bulb.set_rgb(r,g,b)
        return True

    def setSceneTo(self,sceneToApply):
        scenes = []
        with open("scenes.csv", 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                scenes.append(row)
        for scene in scenes:
            if scene[0] == sceneToApply:
                print "Scene", sceneToApply, "found !"
                self.setLightsTo(scene[1],scene[2],scene[3],scene[4])
                return True
        print "This scene doesn't exist"
        return False

port = int(raw_input("Entrez le port d'ecoute : "))
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("127.0.0.1",port))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    if not scheduler:

        sunset = getSunsetTime().split(" ")
        task = [sunset[0],sunset[2],"lightsOn"]
        print "Creation of task :",task

        scheduler = Scheduler(port,"")
        scheduler.addTask(task)
        scheduler.addDailyTask("01:46","updateSunsetTask")
        scheduler.start()

    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
