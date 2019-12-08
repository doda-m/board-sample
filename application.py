from flask import Flask
app = Flask(__name__)

file = open("index.html", "r")
contents = file.read()
file.close()

@app.route("/")
def hello():
    return content
    # return "hello"
