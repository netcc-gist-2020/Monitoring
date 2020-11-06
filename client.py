import asyncio
import websockets

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
    async with websockets.connect("ws://localhost:3000") as websocket:
        await websocket.send("Hi server. I'm client")
        while True:
            data_rcv = await websocket.recv()
            print(data_rcv)

asyncio.get_event_loop().run_until_complete(my_connect())