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
		try:
			for _ in range(1):
				data = {
					'type': "exp",
					'data': {
						'expression': "happy",
						'eye_dir': "center",
						'key': "x91Ljq"
					}
				}
				await websocket.send(json.dumps(data))
				time.sleep(0.1)

		except websockets.exceptions.ConnectionClosedError:
			return
	
websoc_svr = websockets.serve(accept, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(websoc_svr)
asyncio.get_event_loop().run_forever()