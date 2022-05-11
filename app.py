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

app = Flask(__name__, template_folder='templates', static_folder='static')
your_list= []
#app.run(debug=True)

#Podłączenie do bazy danych z kontaktami
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactsDb.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

#Klasa do przechowywania kontaktów
# class Contac(db.Model):
#     id = db.Column("id",db.Integer, primary_key=True)
#     name = db.Column("name",db.String(50))
#     idAddress = db.Column("idAddress",db.String(13))
#     dataOfCreation = db.Column("dataOfCreation",db.DateTime, default = datetime.now)
 
#     def __init__(self,name,idAddress):
#         self.name = name
#         self.idAddress = idAddress

#Klasa do przechowywania kontaktów
class Contac():
    id = 1 
    dataOfCreation = datetime.now
 
    def __init__(self,name,idAddress):
        self.name = name
        self.idAddress = idAddress

class Messeng():

    def __init__(self,side,data):
        self.side=side
        self.data= data
        

@app.route("/", methods=["POST","GET"])
def home():
    print('Strona Głowna', flush=True)

    
    #return render_template('your_view.html', your_list=your_list)


    if request.method == 'POST':
        if request.form.get('action1') == 'Add':
            contakt = Contac(request.form["newContactname"],request.form["newContactIp"])
            print('Jestem w zapytaniu', contakt.name, contakt.idAddress , flush=True)
            # db.session.add (contakt )
            # db.session.commit()     


            return render_template('index.html',your_list=your_list)
           
        elif request.form.get("action2") == "Send" :
            msg = request.form["msg"]
            print('Widomosc do wysania = ', msg , flush=True)
            your_list.append(Messeng('P',msg))
            # db.session.add (contakt )
            # db.session.commit()     


            return render_template('index.html',your_list=your_list)    


        # if request.form.get("addNewContact") == "Dodaj":
    
    else:
        print('Nie udało się pobrać', flush=True)    
        return render_template('index.html',your_list=your_list)
    #return engine.hello()


def serwer(quote): 
    srv = communication.Server('localhost',quote)
    srv.start()
    

def client(quote,messeng):
    communication.Client.sendMesseng('localhost',messeng)

def test():
    counter = 1

    while True:

        print('d', flush=True) 

        time.sleep(1)

        data = 'Zaszyfrowana wiadomosc numer ' + str(counter)

        counter+=1

        pakiet = IpSec(data ,'127.0.0.1')

        pakiet.encryptdata(None)

        communication.Client.sendMesseng('127.0.0.1',pakiet.toBytes())

        odczyatana  = IpSec.fromBytes(q.get())

        print("Wiadomosc  odczyatana",odczyatana.data, flush=True) 





        odszyfrowana = odczyatana.decryptdata(None)

        print("Wiadomosc  odszyfrowana",type(odszyfrowana.data), flush=True) 

        print("Wiadomosc  odszyfrowana",odszyfrowana.data, flush=True) 

if __name__ == '__main__':
    #db.create_all()
    q = Queue()
    t1 = Thread(target = serwer, args =(q,))
    t2 = Thread(target = test, args =())
    t1.start()
    app.run(debug=True)
    