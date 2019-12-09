from flask import Flask, render_template
from flask import request
app = Flask(__name__)

# import pyodbc
# server = 'dodare-db.database.windows.net'
# database = 'signin'
# username = 'dodare'
# password = 'SDN@nitech'
# driver = '{ODBC Driver 13 for SQL Server}'

# cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()

# @app.route("/")
@app.route("/", methods=['GET'])
    return render_template('index.html')

@app.route("/", methods=['POST'])
def indexform():
    if request.form['user'] == "dodare" and request.form['password'] == "sdn":
        return render_template('signin.html')
    else:
        return render_template('index.html')

@app.route("/signin-check")
def signin_check():
    signinhtml = render_template('signin.html')
    return signinhtml

if __name__ == '__main__':
    app.run(debug=True)