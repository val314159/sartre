
from websocket import create_connection
ws = create_connection("ws://echo.websocket.org/")
print "Sending 'Hello, Worldx'..."
ws.send("Hello, Worldx")
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()

