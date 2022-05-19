from datetime import datetime
from urllib import request
from wsgiref.util import request_uri
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
import communication
import sqlite3
import time
from queue import Queue
from threading import Thread
from IpSec import IpSec, Messeng
import socket
import copy


app = Flask(__name__, template_folder='templates', static_folder='static')

#Listy oraz zmiene wykorzystywane do kontaktu z stronami html
your_list= []
contact_list=[]
appMonitor_list = []
netMonitor_list = []
currentTalk=None

class Contac():
    id = 1 
    key = None
    dataOfCreation = datetime.now
    spi = spi=0x0000
 
    def __init__(self,name,ipAddress):
        self.name = name
        self.ipAddress = ipAddress
        

class Messeng():

    def __init__(self,side,data,src,dst):
        self.side=side
        self.data= data
        self.src= src
        self.dst= dst


def serwer(quote,reciveQueue): 
    srv = communication.Server(socket.gethostbyname(socket.gethostname()),reciveQueue)
    srv.start()
    

def client(messeng,currentTalk):
    pakiet = IpSec(messeng ,currentTalk.ipAddress)

    #Zapisywanie komunikatow do kolejski do wyswietlenia w monitorze
    appMonitor.put(str("Uzytkownik chce wyslac widomosc  = "+  messeng))
    appMonitor.put(str("Klucz  = "+  str(currentTalk.key)))
    appMonitor.put(str("SPI  = "+  str(currentTalk.spi)))
    currentTalk.spi+=0x1
    
    
    pakiet.encryptdata(currentTalk.key,currentTalk.spi)
    netMonitor.put(str("Wyslana wiadomosc  = " +  str(pakiet.data) + " na adres " + str(pakiet.dstIP)))
   

    communication.Client.sendMesseng( socket.gethostbyname(socket.gethostname()),pakiet.toBytes())


def addContactsToList():
    print('addContactsToList() is running' , flush=True)
    contact_list.append(Contac("MyAddress",'127.0.0.1'))
    currentTalk = contact_list[0]
    return currentTalk, contact_list




@app.route("/", methods=["POST","GET"])
def home():

    currentTalk, contact_list = addContactsToList()
    print('Strona Głowna',currentTalk.name, flush=True)
    while not  reciveQueue.empty():


        taken = reciveQueue.get()
        netMonitor.put(str("Wiadomosc otrzymana przez serwer  = " +  str(taken.msg.data) + " od " + str(taken.srcIP)))
        

        odszyfrowana = taken.msg.decryptdata(currentTalk.key,currentTalk.spi)
        appMonitor.put(str("otrzymana widomosc  = " +  str(odszyfrowana.data ) ))
       
        your_list.insert(0,Messeng('L',odszyfrowana.data,taken.srcIP, taken.dstIP)) 
    if request.method == 'POST':
        if request.form.get('action1') == 'Add':
            contakt = Contac(request.form["newContactname"],request.form["newContactIp"])
            print('Jestem w zapytaniu', contakt.name, contakt.ipAddress , flush=True)    
            return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk) 
           
        elif request.form.get("action2") == "Send" :
            msg = request.form["msg"]
            print('Widomosc do wysania = ', msg , flush=True)
            if msg !="":
                your_list.insert(0,Messeng('P',msg,str(socket.gethostbyname(socket.gethostname())),currentTalk.ipAddress))
                client(msg,currentTalk)

            return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk) 

        # if request.form.get("addNewContact") == "Dodaj":
    
    else:
        print('Nie udało się pobrać', flush=True)    
        return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk)   




@app.route("/admin", methods=["POST","GET"])
def admin():
    while not  appMonitor.empty():
        taken = appMonitor.get()
        appMonitor_list.insert(0,taken) 

    while not  netMonitor.empty():
        taken = netMonitor.get()
        netMonitor_list.insert(0,taken)     
    
    return render_template('admin.html',appMonitor_list=appMonitor_list,netMonitor_list=netMonitor_list)   
    

if __name__ == '__main__':
    #db.create_all()
    q = Queue()
    reciveQueue= Queue()
    appMonitor = Queue()
    netMonitor = Queue()
  
    t1 = Thread(target = serwer, args =(q,reciveQueue,))
    #t2 = Thread(target = test, args =(reciveQueue,))
    t3 = Thread(target = app.run, args =())
    t1.start()
    #t2.start()
    t3.start()
    
    
    