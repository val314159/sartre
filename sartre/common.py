from prelude import *
from gevent import spawn
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


def glaunch(app,port,ssl_port):
    server = WSGIServer(("0.0.0.0", port), app,
                        handler_class=WebSocketHandler)
    spawn(server.serve_forever)
    server = WSGIServer(("0.0.0.0", ssl_port), app,
                        keyfile='etc/server.key', certfile='etc/server.crt',
                        handler_class=WebSocketHandler)
    server.serve_forever()
    pass

def authorize_token(tok=None,group='user'):
    from bottle import request, abort
    from authenticity.auth_client import valid
    if tok is None: tok = request.params.get('t')
    if not tok:
        print "TOKEN MISSING"
        raise abort(400, 'Missing paramter t (access_token)')
    elif tok == 'VALID':
        print "FAKE VALID"
        return tok
    elif not valid( tok ):
        print "NOT VALID"
        raise abort(401, 'Unauthorized')
    else:
        print "VALID"
        return tok
