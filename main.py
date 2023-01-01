from flask import Flask, request, redirect, flash, session, g
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import os

from flask_login import LoginManager, login_user, login_required

from DataBase import DataBase

class UserLogin():
	def fromDB(self, user_id, db):
		self.__user = db.getUser(user_id)
		return self
	def create(self, user):
		self.__user = user
		return self
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymus(self):
		return False
	def get_id(self):
		return str(self.__user['id'])

DATABASE = '/tmp/BASE.db'
DEBUG = True
SEKRET_KEY = 'd31102076ab7ab894e9c5e4323c0772c562db560'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'BASE.db')))

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	print("load user")
	return UserLogin().fromDB(user_id, dbase)

def connect_db():
	conn = sqlite3.connect(app.config['DATABASE'])
	conn.row_factory = sqlite3.Row
	return conn

def create_db():
	db = connect_db()
	with app.open_resource('sq_db.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	db.close()

def get_db():
	if not hasattr(g, 'link_db'):
		g.link_db = connect_db()
	return g.link_db

dbase = None
@app.before_request
def before_request():
	global dbase
	db = get_db()
	dbase = DataBase(db)

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'link_db'):
		g.link_db.close()

@app.route('/')
@app.route('/Catalog')
@app.route('/Catalog')
def catalog():
	base = connect_db()
	cur = base.cursor()
	product = cur.execute('SELECT * FROM product').fetchall()
	return render_template('Catalog.html', product=product)

@app.route('/Login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		user = dbase.getUserByEmail(request.form['Mail'])
		if user and check_password_hash(user['psw'], request.form['psw']):
			userlogin = UserLogin().create(user)
			login_user(userlogin)
			return redirect('/home')
	return render_template('Login.html')

@app.route('/REGmail', methods=['POST', 'GET'])
def REGmail():
	if request.method == "POST":
		code = request.form['Code']
		if code==pin:
			res = dbase.addUser(nameU, psw, mail)

			if res:
				return redirect('/Login')
			else:
				return "Error"
	else:
		return render_template('REGmail.html')

@app.route('/Registration', methods=['POST', 'GET'])
def reg():
	global nameU
	global psw
	global mail
	global pin
	if request.method == "POST":
		nameU = request.form['Username']
		psw = request.form['Password']
		mail = request.form['Mail']           

		pin = []
		for i in range(6):
			pin.append(random.randint(0,9)) 

		pin = "".join(map(str, pin))

		addr_from = "digatareg@mail.ru"                  
		addr_to   = mail        
		password  = "oq89mNircWEk4PFXvDex"               

		msg = MIMEMultipart()                         
		msg['From']    = addr_from                     
		msg['To']      = addr_to                        
		msg['Subject'] = 'Регистрация на сайт'            

		body = 'Здравствуйте.\n \nНа сайте "digata" был запрос на создание учетной записи с указанием вашего адреса электронной почты.\n \nДля подтверждения новой учетной записи введите следующий код в окне сайта ' + pin + '.\n \nС уважением, администратор сайта.'
		msg.attach(MIMEText(body, 'plain'))            

		server = smtplib.SMTP('smtp.mail.ru', 25)    
		server.set_debuglevel(True) 
		server.starttls()
		server.login(addr_from, password)
		server.send_message(msg)
		server.quit()

		return redirect('/REGmail')
	else:
		return render_template('Registration.html')
	
@app.route('/AboutUs')
def about():
	return render_template('/AboutUs.html')

@app.route('/Basket')
def basket():
	return render_template('/basket.html')

if __name__ == "__main__":
	app.run(debug = True)