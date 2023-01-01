import sqlite3
import time
import math
import re
from flask import url_for

class DataBase:
	def __init__(self, db):
		self.__db = db
		self.__cur = db.cursor()

	def addUser(self, nameU, psw, mail):
		try:
			self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (nameU, psw, mail))
			self.__db.commit()
		except sqlite3.Error as e:
			print("Error")
			return False

		return True

	def getUser(self, user_id):
		try:
			self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
			res = self.__cur.fetchone()
			if not res:
				print("Not user")
				return False

			return res
		except sqlite3.Error as e:
			print("Ошибка получения данных из БД "+str(e))

		return False

	def getUserByEmail(self, mail):
		try:
			self.__cur.execute(f"SELECT * FROM users WHERE mail = {mail} LIMIT 1")
			res = self.__cur.fetchone()
			if not res:
				print("Not user")
				return False

			return res
		except sqlite3.Error as e:
			print("Ошибка получения данных из БД "+str(e))