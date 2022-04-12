from datetime import datetime
import pickle
import copy
import socket
from scapy import all as scapy

class IpSec:
    def __init__(self, data,destination):
        self.destination = destination
        self.data = data #Obiekty klasy Messeng zaszyfrowane lub nie
    
    
    def toBytes(self):
        return pickle.dumps(copy.deepcopy(self))
    
    def fromBytes(self,bytesString):
        return pickle.loads(bytesString)

    def encryptdata(self, key):
        key = b'-\xbd\xb6Q\xa6\x7f6c\x08\xb7\x0coU\xcfg\xcd'
        srcIp = socket.gethostbyname(socket.gethostname())
        sa = scapy.SecurityAssociation(scapy.ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=key)
        p = scapy.IP(str(srcIp), str(self.data.dstIP))
        p /= scapy.UDP(sport=81, dport=80)
        p /= scapy.Raw(copy.deepcopy(self.data))
        p = scapy.IP(scapy.raw(p))
        e = sa.encrypt(p)
        self.data = e

    def decryptdata(self, key):
        key = b'-\xbd\xb6Q\xa6\x7f6c\x08\xb7\x0coU\xcfg\xcd'
        sa = scapy.SecurityAssociation(scapy.ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=key)
        d = sa.decrypt(self.data)
        self.data = d


class Messeng():
    def __init__(self,msg,srcIP,dstIP):
        self.msg = msg
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.time = datetime.now

