#!/usr/bin/env python
# coding: utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(raw_input("Entrez le port d'ecoute : "))
s.connect(("", port))

print("Ecrivez votre message :")
message = raw_input(">> ") # utilisez raw_input() pour les anciennes versions python
s.send(message)
r = s.recv(9999999)
print("Reponse du serveur : %s." % r)
s.close()
