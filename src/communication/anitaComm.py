# coding: utf-8 

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

import threading
import time

class AnitaThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("-> New thread for incomming Anita %s %s" % (self.ip, self.port))

    def depart(self, truc, port):
        self.truc = truc
        self.port = port
        while True:
            self.truc.listen(10)
            print("NetApp server listening on port {}\n").format(self.port) 
            (clientsocket, (ip, port)) = self.truc.accept()
            newthread = AnitaThread(ip, port, clientsocket)
            newthread.start()

    def run(self): 
        print("Connexion de %s %s" % (self.ip, self.port, ))
        r = self.clientsocket.recv(2048)
        prGreen("Received command : %s" % (r))   
        time.sleep(0.5)
        self.clientsocket.send("Response from server with dummy data")
        prGreen("Reply : Response from server with dummy data") 