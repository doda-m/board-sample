from flask import Flask, render_template
from flask import request
app = Flask(__name__)

import pyodbc
server = 'dodare-db.database.windows.net'
database = 'signin'
username = 'dodare'
password = 'SDN@nitech'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

@app.route("/")
def home():
    return render_template('signin.html')

@app.route("/signin", methods=['GET'])
def indexform():
    return render_template('index.html')

@app.route("/signin", methods=['POST'])
def checkinput():
    cursor.execute("SELECT Password FROM SignInTable WHERE UserName='"+request.form['user']+"'")
    dbresponse = cursor.fetchone()
    if dbresponse == None:
        return render_template('signinerr.html')
    if request.form['password'] == dbresponse[0]:
        return render_template('signin.html')
    else:
        return render_template('signinerr.html')

@app.route("/bulletin-board")
def signin_check():
    signinhtml = render_template('signin.html')
    return signinhtml

if __name__ == '__main__':
    app.run(debug=True)