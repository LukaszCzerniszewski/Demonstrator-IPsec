from flask import Flask, render_template
import engine
app = Flask(__name__)
app.run(debug=True)
@app.route("/")
def home():
    return engine.hello()

@app.route("/elo")
def nara():
    return render_template('index.html')

if __name__ == '__main__':
   app.run()