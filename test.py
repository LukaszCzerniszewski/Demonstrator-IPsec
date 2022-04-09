import communication
import os
import subprocess
import time
from threading import Thread
from queue import Queue 


def serwer(quote): 
    srv = communication.Server('localhost',quote)
    srv.start()
    
    
def client(quote,messeng):
    communication.Client.sendMesseng('localhost',messeng)



if __name__ == "__main__":
    q = Queue()
    t1 = Thread(target = serwer, args =(q, ))
    #t2 = Thread(target = client, args =(q,messeng))
    t1.start()
    #t2.start()
    while True:
        communication.Client.sendMesseng('localhost','key exechange 1 ')
        communication.Client.sendMesseng('localhost','key exechange 2')
        time.sleep(1)
        print("Wiadomosc 1",q.get())

    
    
    #print('Server posiada w buforze', srv.msgBuffor)
    #print(p1.stdout)
   
