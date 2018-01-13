#!/usr/bin/env python
# coding: utf-8

import threading
import socket
import time
import datetime
import schedule

class Everyday(threading.Thread):

    def __init__(self,port,ip,time,action):
        threading.Thread.__init__(self)
        schedule.every().day.at(time).do(self.performAction,action)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.ip = ip
        self.s.connect((self.ip, self.port))

    def performAction(self,action):
        self.s.send(action)
        r = self.s.recv(9999999)
        return r

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(30) # wait one minute


class Scheduler(threading.Thread):

    def __init__(self,port,ip):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.ip = ip
        self.taskManager = []
        self.dailyTask = []
        self.s.connect((self.ip, self.port))

    def performAction(self,action):
        self.s.send(action)
        r = self.s.recv(9999999)
        return r

    #A task is a list where the first element in the hour, the second element is the minute, and the third element is the action to be performed
    def addTask(self,task):
        self.taskManager.append(task)

    def getTasks(self):
        return self.taskManager

    def addDailyTask(self,time,action):
        tmp = Everyday(self.port,self.ip,time,action)
        tmp.start()
        self.dailyTask.append(tmp)

    def removeTask(self,task):
        for task in self.taskManager:
            if task[2] == task:
                self.taskManager.remove(task)
                return True
        return False

    def run(self):
        time.sleep(3)
        while(True):
            now = datetime.datetime.now()
            time.sleep(10)
            for task in self.taskManager:
                if now.hour > int(task[0]) or (now.hour >= int(task[0]) and now.minute >= int(task[1])):
                    print "Performing : ", task[2]
                    if(self.performAction(task[2]) == "True"):
                        self.taskManager.remove(task)
"""
port = int(raw_input("Entrez le port d'ecoute : "))
task = Scheduler(port,"");
task.addTask([0,33,"lightsOn"])
task.addTask([0,33,"lightsOff"])
task.addTask([0,33,"isHome"])
task.addDailyTask("01:43","blabla")
task.start()
"""
