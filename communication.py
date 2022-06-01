from ast import Bytes
import socket
import pickle
import os
import sys
from threading import Thread
import time
from IpSec import IKE2, IpSec, Messeng
import pyDH
class Server():
    #ownIpAdress = "127.0.1.1"
    
    #ownIpAdress = "192.168.1.2"
    localPort   = 80
    bufferSize  = 2048
    serverStatus = True
    msgBuffor = None
    def __init__(self,ownIpAdress, quote,netMonitor):
        self.ownIpAdress = ownIpAdress
        self.quote=quote
        self.netMonitor=netMonitor

    
    def start(self):
        self.ownIpAdress = "127.0.1.1" 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ownIpAdress, self.localPort))
        s.listen(1)
        while (True and self.serverStatus == True):
            conn, addr = s.accept()
            
            #print ('Connection address:', addr)
            data = conn.recv(self.bufferSize )
            conn.close()
            if not data: break
            data = pickle.loads(data)
            self.netMonitor.put("Serwer odebral wiadomosc" +  str(data))

            if data[0] == 0 :
                odczyatana = data
                odczyatana[1]  = IpSec.fromBytes(data[1])
                self.quote.put(Messeng(odczyatana,str(addr[0]),str(self.ownIpAdress)))
                #self.quote.put(data)
                #print ("received data:", data)

            
            if data[0] == 1 :
                print ("received data:", data[1], flush=True)
                self.quote.put(Messeng(data,str(addr[0]),str(self.ownIpAdress)))
                d = pyDH.DiffieHellman()
                dh = d.gen_public_key()
                self.quote.put(Messeng([2,dh],str(addr[0]),str(self.ownIpAdress)))
                #conn.send(pickle.dumps('repo'))  # echo
          
                
               

            if data[0] == 2 :
                print ("received data:", data[1], flush=True)
                self.quote.put(Messeng(data,str(addr[0]),str(self.ownIpAdress)))
            
        
            
            
    def stop(self):
        self.serverStatus = False



class Client():
    def sendMesseng(dstIp,data,netMonitor):
        #dstIp =    "127.0.1.1"
        dstIP = "127.0.1.1"
        TCP_PORT = 80
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dstIp, TCP_PORT))
        print("jestem w Kliencie ", data, flush=True)
        netMonitor.put("Klient wysyla widosmoc" +  str(data))
        s.send(pickle.dumps(data))
        #data = s.recv(BUFFER_SIZE)
        s.close()
       # print ("received data:", data)


#Lista komunikatw wysyanych przez Clienta [komunikat,dana]:
    #0 - Wiadomosc
    #1 - KLucz publiczny z wymuszeniem wymiany 
    #2- Klucz publiczny jako odpowiedz


