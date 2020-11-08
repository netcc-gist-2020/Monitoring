
import sqlite3 
class DB:
	def __init__(self):
		self.conn = sqlite3.connect('example.db')
		self.c = self.conn.cursor()


	def create_table(self):
		self.c.execute("create table record (key char(6), expression text, eye_dir text, time datetime default current_timestamp)")
		self.conn.commit()


	def insert(self, record):
		self.c.execute("insert into record (key, expression, eye_dir) values(?,?, ?)", record)


	def query(self):
		return self.c.execute("select * from record")

	def delete_all(self):
		self.c.execute("delete from record")

	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()
		
	def __del__(self):
		self.close()
