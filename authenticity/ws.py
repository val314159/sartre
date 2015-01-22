from bottle import request, response, Bottle, abort, static_file
app = Bottle()

def print_exc():
    import traceback
    print '*'*80
    traceback.print_exc()
    print '*'*80
    pass

def valid(t,g='user'):
    try:
        import requests
        xbase ='s://localhost:9443'
        #xbase = '://localhost:9080'
        s='http%s/auth/valid?t=%s&g=%s'%(xbase,t,g)
        req=requests.get(s)
        return req.status_code==200
    except:
        print_exc()
        return False

class obj:
    @staticmethod
    def ping(*a,**kw):
        return "PONG", repr((a,kw))

    @staticmethod
    def motd(x):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        return y[0]

@app.route('/websocket')
def handle_websocket():

    if valid(request.params.get('t')):
        print "VALID"
    else:
        print "NOT VALID"
        pass

    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            import json
            message = wsock.receive()
            print("Your message was: %r" % message)
            if not message: break
            j=json.loads(message)
            print("Your message was::" + repr(j))

            method=j['method']
            _id=j.get('id',None)
            j['_ws'] = wsock
            fn=getattr(obj,method)
            try:
                ret=fn(j)
                print "RET", repr(ret)
                if ret:
                    wsock.send(json.dumps(dict(id=_id,
                                               method=method,
                                               result=ret)))
                    pass
            except:
                print "EXCEPT"
                print_exc()
        except WebSocketError:
            print "WEB SOCKET ERROR"
            print_exc()
            break
    print "BYE!"

@app.route('/static/<filename>')
def server_static(filename):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return static_file(filename, root='static')

from gevent import spawn
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
spawn(server.serve_forever)
server = WSGIServer(("0.0.0.0", 8443), app,
                    keyfile='etc/server.key', certfile='etc/server.crt',
                    handler_class=WebSocketHandler)
server.serve_forever()
