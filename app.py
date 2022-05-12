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
your_list= []
contact_list=[]
currentTalk=None
#app.run(debug=True)

#Podłączenie do bazy danych z kontaktami
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactsDb.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

#Klasa do przechowywania kontaktów
# class Contac(db.Model):
#     id = db.Column("id",db.Integer, primary_key=True)
#     name = db.Column("name",db.String(50))
#     ipAddress = db.Column("ipAddress",db.String(13))
#     dataOfCreation = db.Column("dataOfCreation",db.DateTime, default = datetime.now)
 
#     def __init__(self,name,ipAddress):
#         self.name = name
#         self.ipAddress = ipAddress

#Klasa do przechowywania kontaktów
class Contac():
    id = 1 
    dataOfCreation = datetime.now
 
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
    pakiet.encryptdata(None)
    #communication.Client.sendMesseng(currentTalk.ipAddress,pakiet.toBytes())
    communication.Client.sendMesseng( socket.gethostbyname(socket.gethostname()),pakiet.toBytes())

def test(reciveQueue):
    counter = 1

    while True:

        print('d', flush=True) 

        time.sleep(4)

        data = 'Zaszyfrowana wiadomosc numer ' + str(counter)

        counter+=1

        pakiet = IpSec(data ,'127.0.0.1')

        pakiet.encryptdata(None)

        communication.Client.sendMesseng('127.0.0.1',pakiet.toBytes())

        # odczyatana  = IpSec.fromBytes(q.get())
        
        #print("Wiadomosc  odczyatana",odczyatana.data, flush=True) 

        # odszyfrowana = odczyatana.decryptdata(None)

        #print("Wiadomosc  odszyfrowana",type(odszyfrowana.data), flush=True) 

        # print("Wiadomosc  odszyfrowana",odszyfrowana.data, flush=True) 
        # reciveQueue.put(odszyfrowana.data)


def addContactsToList():
    print('addContactsToList() is running' , flush=True)
  
    contact_list.append(Contac("MyAddress",'127.0.0.1'))
    currentTalk = contact_list[0]
    return currentTalk, contact_list




@app.route("/", methods=["POST","GET"])
def home():

    currentTalk, contact_list = addContactsToList()
    print('Strona Głowna',currentTalk.name, flush=True)

    
    #return render_template('your_view.html', your_list=your_list)
    while not  reciveQueue.empty():
        #Trzeba zamienic, zeby przekazywalo przez quote od kogo msg
        #your_list.insert(0,Messeng('L',reciveQueue.get(),currentTalk.ipAddress, socket.gethostbyname(socket.gethostname()))) 
        #your_list.insert(0,copy.deepcopy(reciveQueue.get()))

        taken = reciveQueue.get()
        your_list.insert(0,Messeng('L',taken.msg,taken.srcIP, taken.dstIP)) 
    if request.method == 'POST':
        if request.form.get('action1') == 'Add':
            contakt = Contac(request.form["newContactname"],request.form["newContactIp"])
            print('Jestem w zapytaniu', contakt.name, contakt.ipAddress , flush=True)
            # db.session.add (contakt )
            # db.session.commit()     
            return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk) 
           
        elif request.form.get("action2") == "Send" :
            msg = request.form["msg"]
            print('Widomosc do wysania = ', msg , flush=True)
            if msg !="":
                your_list.insert(0,Messeng('P',msg,str(socket.gethostbyname(socket.gethostname())),currentTalk.ipAddress))
                client(msg,currentTalk)
            # db.session.add (contakt )
            # db.session.commit()     


            return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk) 

        # if request.form.get("addNewContact") == "Dodaj":
    
    else:
        print('Nie udało się pobrać', flush=True)    
        return render_template('index.html',your_list=your_list, contact_list=contact_list, currentTalk=currentTalk)   
    #return engine.hello()






if __name__ == '__main__':
    #db.create_all()
    q = Queue()
    reciveQueue= Queue()
  
    t1 = Thread(target = serwer, args =(q,reciveQueue,))
    #t2 = Thread(target = test, args =(reciveQueue,))
    t3 = Thread(target = app.run, args =())
    t1.start()
    #t2.start()
    t3.start()
    
    #app.run(debug=True)
    