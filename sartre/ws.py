from gevent import monkey;monkey.patch_all()
from prelude import *
from bottle import request, response, Bottle, abort, static_file, redirect
app = Bottle()

def DB(_=[]):
    from leveldb import LevelDB
    if not _: _.append(LevelDB('.db'))
    return _[0]

class obj:
    @staticmethod
    def db_create(ws,rec):
        print  "DB CREATE", repr(rec)
        obj_id = obj.pop('id')
        DB().Put(obj_id+'.~meta', '{}')
        for k,v in obj.iteritems():
            DB().Put(obj_id+'.'+k, json.dumps(v))
            pass
        return "DB CREATE", repr(rec)
    @staticmethod
    def db_read(ws,rec):
        print  "DB READ", repr(rec)
        return "DB READ", repr(rec)
    @staticmethod
    def db_update(ws,rec):
        print  "DB UPDATE", repr(rec)
        print  "DB UPDATE", repr(rec['params'])
        obj_id=obj.pop('id')
        for k,v in obj.iteritems():
            print "----- UP", repr((k,v))
            DB().Put(obj_id+'.'+k, json.dumps(v))
            pass
        return "DB UPDATE"
    @staticmethod
    def db_delete(ws,rec):
        print  "DB DELETE", repr(rec)
        DB().Delete(rec['id'])
        return "DB DELETE", repr(rec)

    @staticmethod
    def sub(*a,**kw):
        return "SUB", repr((a,kw))
    @staticmethod
    def pub(*a,**kw):
        return "PUB", repr((a,kw))

    @staticmethod
    def ping(*a,**kw):
        return "PONG", repr((a,kw))
    @staticmethod
    def load(ws,path):
        print "LOAD", repr(path)
        data=open(path).read()
        arr=path.split('/')
        d = dict(
            dirname='/'.join(arr[:-1]),
            filename=arr[-1],
            data=data,
            )
        print "D", repr(d)
        return d
    @staticmethod
    def save(ws,filename, data):
        f=open(filename,'w')
        f.write(data)
        f.close()
        return dict(result=true)

    @staticmethod
    def filesystem_walk(ws,x):
        return dict((name,(dirs,files))
                    for name,dirs,files in os.walk(x))
    @staticmethod
    def fortune(ws):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        return y[0]
    pass

_ClientObj=obj
def set_client_obj(obj):global _ClientObj;_ClientObj=obj
set_client_obj(obj)

from common import authorize_token
from geventwebsocket import WebSocketError

@app.route('/')
def index():
    return redirect('/static/index.html')

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
    print "BYE!"

@app.route('/README.md')
@app.route('/static/<filename:path>')
def serve_static(filename=None):
    from markdown2 import markdown_path
    if filename is None  or  filename.endswith('.md'):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return markdown_path('static/'+filename if filename else 'README.md')
    resp = static_file(filename, root='static/')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def dump_db():
    print "DUMP DB"
    for x in DB().RangeIter():
        print "X", x

from common import glaunch
if __name__=='__main__':
    print 'DB0', '='*80
    dump_db()
    print 'DB9', '='*80
    glaunch(app,8080,8443)
