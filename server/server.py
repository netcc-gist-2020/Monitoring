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
	try: 
		data_rcv = await websocket.recv()
		json_data = json.loads(data_rcv)
		if json_data["type"] == "open":
			data_send = {
					'type': "welcome",
					'data': {
						'key': None,
						'keys': None,
						'expression': None, 
					}
				}
			await websocket.send(json.dumps(data_send))
	except json.decoder.JSONDecodeError:
		print("json decode error")
	while True:
		try:
			for _ in range(1):
				data = {
					'type': "exp",
					'data': {
						'expression': "neutral",
						'eye_dir': "center",
						'key': "a91Ljq"
					}
				}
				await websocket.send(json.dumps(data))
				time.sleep(0.1)

		except websockets.exceptions.ConnectionClosedError:
			return
	
websoc_svr = websockets.serve(accept, "0.0.0.0", 3000)

asyncio.get_event_loop().run_until_complete(websoc_svr)
asyncio.get_event_loop().run_forever()
