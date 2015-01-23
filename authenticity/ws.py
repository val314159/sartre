from prelude import *
from bottle import request, response, Bottle, abort, static_file
app = Bottle()
print 00001
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
    pass

_ClientObj=obj
def set_client_obj(obj):global _ClientObj;_ClientObj=obj
set_client_obj(obj)

from common import authorize_token

@app.route('/test')
def test():
    response.headers['Access-Control-Allow-Origin'] = '*'
    tok = authorize_token(None)
    return ['ok']

@app.route('/websocket')
def handle_websocket():
    response.headers['Access-Control-Allow-Origin'] = '*'

    tok = authorize_token()

    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print("Your message was: %r" % message)
            if not message: break
            j=json.loads(message)
            print("Your message was::" + repr(j))

            method=j['method']
            _id=j.get('id',None)
            j['_ws'] = wsock
            fn=getattr(client_obj,method)
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
def serve_static(filename):
    resp = static_file(filename, root='static')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

from common import glaunch
print 100001
if __name__=='__main__':glaunch(app,8080,8443)
