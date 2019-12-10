# import flask framework
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    pass

# import driver for database
import pyodbc

# configure database information
server = 'dodare-db.database.windows.net'
database = 'signin'
username = 'dodare'
password = 'SDN@nitech'
driver = '{ODBC Driver 17 for SQL Server}'

# connect database
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Home page
@app.route("/")
def home():
    return render_template('home.html')

# Login page(GET)
@app.route("/login", methods=['GET'])
def indexform():
    return render_template('login.html')

# Login page(POST)
# If user submit Username and Password,
# server check it.
@app.route("/login", methods=['POST'])
def checkinput():
    # request Password against Username to database
    cursor.execute("SELECT Password FROM SignInTable WHERE UserName='"+request.form['user']+"'")
    dbresponse = cursor.fetchone()
    # Does Username exist?
    if dbresponse == None:
        return render_template('loginerr.html')
    # Is Password correct?
    if request.form['password'] == dbresponse[0]:
        return render_template('login.html')
    else:
        return render_template('loginerr.html')

# Bulletin board page
@app.route("/bulletin-board")
@login_required
def bulletin_board():
    signinhtml = render_template('login.html')
    return signinhtml

if __name__ == '__main__':