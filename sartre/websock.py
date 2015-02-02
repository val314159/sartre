from prelude import *
from obj import obj
from geventwebsocket import WebSocketError
from gevent import spawn
from obj import obj

_ClientObj=obj
def set_client_obj(obj):global _ClientObj;_ClientObj=obj
set_client_obj(obj)

def process(tok,wsock):
    while True:
        try:
            message = wsock.receive()
            if not message: break
            j=json.loads(message)

            method=j['method']
            _id=j.get('id',None)
            j['_ws'] = wsock
            fn=getattr(_ClientObj,method)
            try:
                params = j['params']
                if type(params) in (type([]),type(())):
                    ret=spawn(fn,wsock,_id,*params)
                else:
                    ret=spawn(fn,wsock,_id,**params)
                    pass
            except:
                print_exc()
                break
        except WebSocketError:
            print_exc()
            break
        pass
    print "BYE!"
    pass
