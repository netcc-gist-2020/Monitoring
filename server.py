import asyncio
import websockets
import json
import time

'''
# exp
JSON {
 'type': "exp"
 'data' : JSON {
   'key': "exp를 보낸놈의 ID"
   'keys': null
   'expression': "expression"
 }
}

# 
'''

async def accept(websocket, path):
    #data_rcv = await websocket.recv()
    while True:
        for _ in range(10):
            data = {
                'type': "exp",
                'data': {
                    'key': "AX1FZX",
                    'keys': None,
                    'expression': "sleepy"
                }
            }
        await websocket.send(json.dumps(data))
        time.sleep(1)
    
websoc_svr = websockets.serve(accept, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(websoc_svr)
asyncio.get_event_loop().run_forever()