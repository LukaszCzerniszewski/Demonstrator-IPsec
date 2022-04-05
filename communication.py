import socket
import pickle
from esp import Esp


class server():
    #ownIpAdress = "192.168.1.2"
    localPort   = 80
    bufferSize  = 1024
    serverStatus = True
    def __init__(self,ownIpAdress):
        self.ownIpAdress = ownIpAdress

    
    def start(self):
        # Create a datagram socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((self.ownIpAdress, self.localPort))
        print("UDP server up and listening")
        while(True and self.serverStatus == True):
            bytesAddressPair = UDPServerSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientIP  = "Client IP Address:{}".format(address)
            print(clientIP)
            mess =pickle.loads(message)
            # Sending a reply to client
            #UDPServerSocket.sendto(bytesToSend, address)
    
    def stop(self):
        self.serverStatus = False


#udp klient to send pakiets
class Client():
    def sendMesseng(self,dstIp,data):   
        dstIp = "192.168.1.2" 
        serverAddressPort   = (dstIp, 80)
        bufferSize          = 1024
        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        UDPClientSocket.sendto(pickle.dumps(data), serverAddressPort)
        #Answer from server
        #msgFromServer = UDPClientSocket.recvfrom(bufferSize)
       # msg = "Message from Server {}".format(msgFromServer[0])
       #print(msg)


