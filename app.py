from datetime import datetime
from urllib import request
from wsgiref.util import request_uri
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
import communication
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static')
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

@app.route("/", methods=["POST","GET"])
def home():
    print('Strona Głowna', flush=True)
    if request.method == 'POST':
        if request.form.get('action1') == 'Add':
            contakt = Contac(request.form["newContactname"],request.form["newContactIp"])
            print('Jestem w zapytaniu', contakt.name, contakt.idAddress , flush=True)
            # db.session.add (contakt )
            # db.session.commit()     


            return render_template('index.html')
           
        elif request.form.get("action2") == "Send" :
            msg = request.form["msg"]
            print('Widomosc do wysania = ', msg , flush=True)
            # db.session.add (contakt )
            # db.session.commit()     


            return render_template('index.html')    


        # if request.form.get("addNewContact") == "Dodaj":
    
    else:
        print('Nie udało się pobrać', flush=True)    
        return render_template('index.html')
    #return engine.hello()




if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
    