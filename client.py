import asyncio
import websockets
import sqlite3 
import json

'''
Request Form when Enter
JSON {
 'type': "open"
 'data' : JSON {
   'key': null
   'keys': null
   'expression': null
 }
}
'''

class DB:
	def __init__(self):
		self.conn = sqlite3.connect('example.db')
		self.c = self.conn.cursor()


	def create_table(self):
		self.c.execute("create table record (key char(6), data text, time datetime default current_timestamp)")
		self.conn.commit()


	def insert(self, record):
		self.c.execute("insert into record values(?,?,NULL)", record)


	def query(self):
		return self.c.execute("select * from record")

	def delete_all(self):
		self.c.execute("delete from record")

	def commit(self):
		self.conn.commit()


"""
async def my_connect(db):
    async with websockets.connect("ws://localhost:3001") as websocket:
    	while True:
        	received_data = await websocket.recv()
"""

async def my_connect(db):
    async with websockets.connect("ws://localhost:3000") as websocket:
        #await websocket.send("Hi server. I'm client")

        while True:
            data_rcv = await websocket.recv()
            
            data_rcv = json.loads(data_rcv)

            data_rcv = data_rcv["data"]

            data_rcv["key"]
            data_rcv["exp"]
            print(data_rcv)



if __name__ == "__main__":
	db = DB()
	asyncio.get_event_loop().run_until_complete(my_connect(db))


