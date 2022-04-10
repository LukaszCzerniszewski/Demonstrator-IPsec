from flask import Flask, render_template
import communication
app = Flask(__name__, template_folder='templates', static_folder='static')
app.run(debug=True)
@app.route("/")
def home():
    
    return render_template('index.html')
    #return engine.hello()

@app.route("/elo")
def nara():
    return 'Weronika <3'
    #return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)