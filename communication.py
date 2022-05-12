import socket
import pickle
import os
import sys
from IpSec import IpSec, Messeng
class Server():
    ownIpAdress = "127.0.0.1"
    localPort   = 5005
    bufferSize  = 1024
    serverStatus = True
    msgBuffor = None
    def __init__(self,ownIpAdress, quote):
        self.ownIpAdress = ownIpAdress
        self.quote=quote

    
    def start(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ownIpAdress, self.localPort))
        s.listen(1)
        while (True and self.serverStatus == True):
            conn, addr = s.accept()
            #print ('Connection address:', addr)
            data = conn.recv(self.bufferSize )
            if not data: break
            odczyatana  = IpSec.fromBytes(data)
            odszyfrowana = odczyatana.decryptdata(None)
            self.quote.put(Messeng(odszyfrowana.data,str(addr[0]),str(self.ownIpAdress)))
            #self.quote.put(data)
            #print ("received data:", data)
            conn.send(pickle.dumps('repo'))  # echo
            conn.close()
     
        conn.close()
     
            
            
    def stop(self):
        self.serverStatus = False



class Client():
    def sendMesseng(dstIp,data):   
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dstIp, TCP_PORT))
        s.send(data)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print ("received data:", data)







  