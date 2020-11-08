import asyncio
import websockets
import json
from db import DB

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
socket_url = "0.0.0.0"
# socket_url = "localhost"

async def connect_socket(db):
	async with websockets.connect("ws://localhost:3000") as websocket:
		while True:
			try:
				data_rcv = await websocket.recv()
				json_data = json.loads(data_rcv)
				data = json_data["data"]

				key = data["key"]
				expression = data["expression"]
				eye_dir = data["eye_dir"]

				db.insert((key, expression, eye_dir))

			except websockets.exceptions.ConnectionClosedError:
				return

async def save_db(db, print_log=True):
	while True:
		if print_log:
			for row in db.query():
				print(row)
			print("Saved!")

		db.commit()
		# why does it needed? await asyncio.sleep(1) do anything for this situation cause it's noas
		await asyncio.sleep(1)

async def accept_user(websocket, path):
	while True:
		msg = await websocket.recv()
			if msg == "hello":
		await websocket.send("welcome")
		print("connection established!")
		db = DB()
		try:
			db.create_table()	# create the table if it doesn't exist
		except:
			pass
		# connect to socket
		socket_connection = asyncio.ensure_future(connect_socket(db))
		savedb = asyncio.ensure_future(save_db(db))
		while True:
			try:
				data_rcv = await websocket.recv()
				
				if "cancel" in data_rcv:
					await websocket.send("good-bye")
					print("received cancel request")
					break
			except websockets.exceptions.ConnectionClosedError:
				print("cancelled!")
				break
		socket_connection.cancel()
		savedb.cancel()
		await asyncio.sleep(5)
		db.delete_all()

async def main():
	ws = asyncio.ensure_future(websockets.serve(accept_user, socket_url, 3001))
	while True:
		await asyncio.sleep(1)

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())