from flask import Flask
app = Flask(__name__)

file = open("index.html", "r")
indexhtml = file.read()
file.close()

@app.route("/")
def index():
    return indexhtml
    # return "hello"
