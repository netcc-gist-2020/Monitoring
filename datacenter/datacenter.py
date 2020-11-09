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
# real socket server "116.89.189.47:8080"
# socket server url
socket_url = "116.89.189.47"
# socket_url = "localhost"

async def connect_socket(db):
	before_time = datetime.now()
	async with websockets.connect("ws://localhost:3000") as websocket:
		try:
			handshake = {
				'type': 'open',
				'data': {
					'key': None,
					'keys': None,
					'expression': None
				}
			}
			await websocket.send(json.dumps(handshake))
			data_rcv = await websocket.recv()
			print(data_rcv)
			data_rcv = json.loads(data_rcv)
			

		except websockets.exceptions.ConnectionClosedError:
			return

	print(f"ws://{socket_url}:3000")
	async with websockets.connect(f"ws://{socket_url}:3000") as websocket:
		while True:
			try:
				data_rcv = await websocket.recv()
				print(data_rcv)
				json_data = json.loads(data_rcv)
				if json_data["type"] == "exp":
					data = json_data["data"]

					key = data["key"]
					expression = data["expression"]
					eye_dir = data["eye_dir"]

					print(db.insert(key, expression, eye_dir, seconds))
					key = data["key"]
					expression = data["expression"]
					eye_dir = data["eye_dir"]

					print(db.insert(key, expression, eye_dir))

			except websockets.exceptions.ConnectionClosedError:
				return

async def save_db(db, print_log=True):
	while True:
		if print_log:
			for row in db.query():
				print(row)
			print("Saved!")
		await asyncio.sleep(1)

async def accept_user(websocket, path):
	
	while True:
		try:
			msg = await websocket.recv()
			if msg == "hello":
				await websocket.send("welcome")
				break
		except websockets.exceptions.ConnectionClosedError:
			return

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
	
	db.delete_all()
	while not socket_connection.cancelled():
		print("@@")
		await asyncio.sleep(1)
	print("socket_connection cancelled!")

async def main():
	ws = asyncio.ensure_future(websockets.serve(accept_user, "0.0.0.0", 3001))
	while True:
		await asyncio.sleep(1)

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())