# import flask framework
from flask import Flask, render_template, request, session, redirect, url_for
# from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# import driver for database
import pyodbc

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

username = set()

# manage login user
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# configure database information
dbserver = 'dodare-db.database.windows.net'
database = 'signin'
dbusername = 'dodare'
password = 'SDN@nitech'
driver = '{ODBC Driver 17 for SQL Server}'

# connect database
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+dbserver+';PORT=1433;DATABASE='+database+';UID='+dbusername+';PWD='+ password)
cursor = cnxn.cursor()

# def set_password(self, password):
#     self.password_hash = generate_password_hash(password)

# def check_password(self, password):
#     return check_password_hash(self.password_hash, password)


# class User(UserMixin):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.passward = password

# Home page
@app.route("/")
def home():
    if 'username' in session:
        return render_template('home-login.html')
    else:
        return render_template('home.html')

# Login page(GET)
@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

# Login page(POST)
# If user submit Username and Password,
# server check it.
@app.route("/login", methods=['POST'])
def logincheck():
    # request Password against Username to database
    username = request.form['user']
    password = request.form['password']
    cursor.execute("SELECT * FROM SignInTable WHERE UserName='"+username+"' AND Password='"+password+"'")
    dbresponse = cursor.fetchone()
    # Does Username exist?
    if dbresponse == None:
        return render_template('loginerr.html')
    # Is Password correct?
    if request.form['password'] == dbresponse[1]:
        session['username'] = username
        return redirect("/")
    else:
        return render_template('loginerr.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Bulletin board page
@app.route("/bulletin-board")
def bulletin_board():
    if 'username' in session:
        return render_template('bulletin-board.html',user=session['username'])
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)