from datetime import datetime
import pickle
import copy
import socket
import pyDH
from scapy import all as scapy
import time



class IpSec:
    
    def __init__(self, data,dstIP):
        self.data = data #Obiekty klasy Messeng zaszyfrowane lub nie
        self.srcIP = str(socket.gethostbyname(socket.gethostname()))
        self.dstIP = dstIP
        self.time = datetime.now

  

    def toBytes(self):
        return pickle.dumps(copy.deepcopy(self))

    

    def fromBytes(bytesString):
        return pickle.loads(bytesString)





    def encryptdata(self, key, spi):
        p = scapy.IP(src=self.srcIP , dst=self.dstIP )
        p /= scapy.TCP(sport=81, dport=80)
        p /= scapy.Raw(self.data)
        p = scapy.IP(scapy.raw(p))
        sa = scapy.SecurityAssociation(scapy.ESP, spi= spi, crypt_algo='AES-CBC', crypt_key=key)
        e = sa.encrypt(p)
        self.data = e
        return self



    def decryptdata(self, key, spi):
        sa = scapy.SecurityAssociation(scapy.ESP, spi=spi, crypt_algo='AES-CBC', crypt_key=key)
        d = sa.decrypt(self.data)
        #self.data = str(d[2])[2:-1]
        try:
            self.data = str(d[2])[2:-1]
        except:
            print("Bald odczytu len = ", len(d), "affw",d, flush=True)
        return self




class Messeng():

    def __init__(self,msg,srcIP,dstIP):
        self.msg = msg
        self.srcIP = srcIP
        self.dstIP = dstIP


    def toBytes(self):
        return pickle.dumps(copy.deepcopy(self))



    def __bytes__(self):
        return pickle.dumps(copy.deepcopy(self))



    def fromBytes(bytesString):
        return pickle.loads(bytesString)



class IKE2():
    currentKey = b'\x80\x04\x95D\x00\x00\x00\x00\x00\x00\x00\x8c@953' 
    lastKeyExchange = None
    dH = pyDH.DiffieHellman()
    pubkey = None
    
    def __init__(self) -> None:
        pass  

    def generatePublicKey(self):
        self.pubkey = self.dH.gen_public_key()
        return self.pubkey


    def generatePrivateKey(self,inComeKey):
        self.currentKey = self.dH.gen_shared_key(inComeKey)
        self.currentKey  = pickle.dumps(self.currentKey)[0:16]
        self.lastKeyExchange = time.time()
        return self.currentKey


   
   