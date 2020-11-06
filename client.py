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


async def my_connect(db):
	async with websockets.connect("ws://localhost:3000") as websocket:
		#await websocket.send("Hi server. I'm client")

		while True:
			data_rcv = await websocket.recv()
			json_data = json.loads(data_rcv)
			data = json_data["data"]

			key = data["key"]
			expression = data["expression"]
			eye_dir = data["eye_dir"]

			db.insert((key, expression, eye_dir))

			


async def main():
	db = DB()
	try:
		db.create_table()
	except:
		pass


	asyncio.ensure_future(my_connect(db))
	while True:
		await asyncio.sleep(1)

		q = db.query()
		for row in q:
			print(row)

		db.commit()

		print("Data saved!")


	app.run(host='127.0.0.1', port='3001')


if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())


