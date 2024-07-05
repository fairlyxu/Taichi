import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid

def open_websocket_connection():
  #server_address='127.0.0.1:8188'
  server_address = '183.136.222.99:5001'
  client_id=str(uuid.uuid4())

  ws = websocket.WebSocket()
  ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
  return ws, server_address, client_id