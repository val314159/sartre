from prelude import *
from obj import obj
from geventwebsocket import WebSocketError

from obj import obj

_ClientObj=obj
def set_client_obj(obj):global _ClientObj;_ClientObj=obj
set_client_obj(obj)

def process(tok,wsock):
    while True:
        try:
            message = wsock.receive()
            #print("Your message was: %r" % message)
            if not message: break
            j=json.loads(message)
            #print("Your message was::" + repr(j))

            method=j['method']
            _id=j.get('id',None)
            j['_ws'] = wsock
            fn=getattr(_ClientObj,method)
            try:
                print 'J'*60
                print '------', repr(j)
                print 'J'*60
                params = j['params']
                if type(params) in (type([]),type(())):
                    ret=fn(wsock,*params)
                else:
                    ret=fn(wsock,**params)
                    pass
                #print "RET", repr(ret)
                if ret:
                    wsock.send(json.dumps(dict(id=_id,
                                               method=method,
                                               result=ret)))
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
