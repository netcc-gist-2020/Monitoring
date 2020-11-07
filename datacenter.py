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

async def connect_socket(db):
	async with websockets.connect("ws://localhost:3000") as websocket:
		#await websocket.send("Hi server. I'm client")

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



async def accept_user(websocket, path):
	print("connection established!")

	db = DB()

	try:
		db.create_table()	# create the table if it doesn't exist
	except:
		pass

	# connect to socket
	socket_connection = asyncio.ensure_future(connect_socket(db))

	while True:
		try:
			data_rcv = await websocket.recv()
			if data_rcv.contains("cancel"):
				print("received cancel request")
				break

		except websockets.exceptions.ConnectionClosedError:
			print("canceled!")
			break

	socket_connection.cancel()
	


async def main():
	ws = asyncio.ensure_future(websockets.serve(accept_user, "localhost", 3001))

	while True:
		await asyncio.sleep(1)


if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())


