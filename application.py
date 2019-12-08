from flask import Flask, render_template
app = Flask(__name__)

# file = open("index.html", "r")
# indexhtml = file.read()
# file.close()

@app.route("/")
def index():
    indexhtml = render_template('index.html')
    return indexhtml
    # return "hello"

@app.route("/signin-check")
def signin_check():
    signinhtml = render_template('signin.html')
    return signinhtml

if __name__ == '__main__':
    app.run(debug=True)