# import flask framework
from flask import Flask, render_template,\
	request, session, redirect, url_for
from flask_sslify import SSLify

import os
# from flask_login import LoginManager, login_user, \
#   logout_user, login_required, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# import driver for database
import pyodbc

app = Flask(__name__)
app.secret_key = os.urandom(24)
sslify = SSLify(app)
# username = set()

# configure database information
dbserver = 'dodare-db.database.windows.net'
database = 'signin'
dbusername = 'dodare'
dbpassword = 'SDN@nitech'
dbdriver = '{ODBC Driver 17 for SQL Server}'

# connect database
# cnxn = pyodbc.connect('\
# 	DRIVER='+dbdriver+';\
# 	SERVER='+dbserver+';\
# 	PORT=1433;\
# 	DATABASE='+database+';\
# 	UID='+dbusername+';\
# 	PWD='+ dbpassword)
# cursor = cnxn.cursor()

# Home page
@app.route("/")
def home():
	if 'username' in session:
		return render_template('home.html',state="Login")
	else:
		return render_template('home.html',state="Logout")
	# return render_template('home.html')

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
	passwd = request.form['password']
	# cursor.execute("\
	# 	SELECT * \
	# 	FROM SignInTable \
	# 	WHERE UserName='"+username+"' \
	# 	AND Password='"+passwd+"'") 
	# dbresponse = cursor.fetchone()
	dbresponse = True
	# Does User exist?
	if dbresponse == None:
		return render_template('loginerr.html')
	else:
		session['username'] = username
		return redirect("/")

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