
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

async def my_connect():
	async with websockets.connect("ws://localhost:3001") as websocket:
		#await websocket.send("Hi server. I'm client")

		while True:
			data_rcv = await websocket.recv()


async def main():
	asyncio.ensure_future(my_connect())
	while True:
		await asyncio.sleep(1)


if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())