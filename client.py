import asyncio
import websockets

async def my_connect():
    async with websockets.connect("ws://localhost:3000") as websocket:
        for _ in range(1,100,1):
            await websocket.send("Hi server. I'm client")
            data_rcv = await websocket.recv()
            print(data_rcv)

asyncio.get_event_loop().run_until_complete(my_connect())