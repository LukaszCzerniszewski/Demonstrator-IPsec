from datetime import datetime
import pickle
import copy
import socket
from scapy.compat import raw
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.ipsec import SecurityAssociation, ESP, AH
from scapy.packet import Raw
from scapy.sendrecv import send, sr





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

    





    def encryptdata(self, key):

        key = b'-\xbd\xb6Q\xa6\x7f6c\x08\xb7\x0coU\xcfg\xcd'

        #srcIp = socket.gethostbyname(socket.gethostname())

        #print(str(srcIp),self.data.dstIP)

        p = IP(src=self.srcIP , dst=self.dstIP )

        p /= TCP(sport=81, dport=80)

        p /= Raw(self.data)

        p = IP(raw(p))

        sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=key)

        e = sa.encrypt(p)

        self.data = e

        return self



    def decryptdata(self, key):

        key = b'-\xbd\xb6Q\xa6\x7f6c\x08\xb7\x0coU\xcfg\xcd'

        sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=key)

        d = sa.decrypt(self.data)

        self.data = str(d[2])[2:-1]

        return self





class Messeng():

    def __init__(self,msg,srcIP,dstIP):

        self.msg = msg

        

    

    def toBytes(self):

        return pickle.dumps(copy.deepcopy(self))



    def __bytes__(self):

        return pickle.dumps(copy.deepcopy(self))



    def fromBytes(bytesString):

        return pickle.loads(bytesString)

