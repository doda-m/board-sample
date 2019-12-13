import os
import datetime

# import flask framework
from flask import Flask, render_template,\
	request, session, redirect, url_for, Markup
from flask_sslify import SSLify

# import driver for database
import pyodbc

app = Flask(__name__)
app.secret_key = os.urandom(24)
sslify = SSLify(app)

# configure database information
dbserver = 'dodare-db.database.windows.net'
database = 'signin'
dbusername = 'dodare'
dbpassword = 'SDN@nitech'
dbdriver = '{ODBC Driver 17 for SQL Server}'

# connect database
cnxn = pyodbc.connect('\
	DRIVER='+dbdriver+';\
	SERVER='+dbserver+';\
	PORT=1433;\
	DATABASE='+database+';\
	UID='+dbusername+';\
	PWD='+ dbpassword)
cursor = cnxn.cursor()

# Home page
@app.route("/")
def home():
	if 'username' in session:
		return render_template('home.html',\
			state="Login",user=session['username'])
	else:
		return render_template('home.html', state="Logout")

# Login page(GET)
@app.route("/login", methods=['GET'])
def login():
	if 'username' in session:
		return redirect("/")
	return render_template('login.html',state="Logout")

# Login page(POST)
# If user submit Username and Password, server check it.
@app.route("/login", methods=['POST'])
def logincheck():
	username = request.form['user']
	passwd = request.form['password']
	cursor.execute("\
		SELECT * \
		FROM SignInTable \
		WHERE UserName=? \
		AND Password=?",\
		username, passwd
	) 
	usercheck = cursor.fetchone()
	# Does User exist?
	if usercheck == None:
		return render_template('loginerr.html',state="Logout")
	else:
		session['username'] = username
		return redirect("/")

# Logout page
@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect("/")

# Bulletin board page
@app.route("/bulletin-board",methods=['GET'])
def bulletin_board():
	today = datetime.date.today()
	# Get today's posts
	cursor.execute("\
		SELECT * FROM PostsTable\
		WHERE Date=?",\
		today
	)
	tdposts = cursor.fetchall()
	for row in tdposts:
		row.Messege = Markup(row.Messege.replace('\r\n', '<br>'))

	# Get posts before today
	cursor.execute("\
		SELECT * FROM PostsTable\
		WHERE Date<?",\
		today
	)
	hstposts = cursor.fetchall()
	for row in hstposts:
		row.Messege = Markup(row.Messege.replace('\r\n', '<br>'))
	if 'username' in session:
		return render_template('bulletin-board.html', state="Login",\
			user=session['username'], msgs=tdposts, historymsgs=hstposts,\
			date=datetime.date.today())
	else:
		return render_template('bulletin-board.html', state="Logout",\
			msgs=tdposts, historymsgs=hstposts, date=datetime.date.today())

@app.route("/bulletin-board",methods=['POST'])
def bulletin_board_post():
	if 'username' in session:
		postmsg = request.form.get('content', None)
		now = datetime.datetime.today()
		postdate = now.date()
		posttime = now.time()
		cursor.execute("\
			INSERT INTO PostsTable(UserName, Date, Time, Messege)\
			VALUES (?,?,?,?)",\
			session['username'], postdate, posttime, postmsg\
		)
		cnxn.commit()
		return redirect("/bulletin-board")
	else:
		return redirect("/login")
	
if __name__ == '__main__':
	app.run(debug=True)