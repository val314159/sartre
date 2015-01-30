if __name__=='__main__':
    from gevent import monkey;monkey.patch_all()
    pass
import os, sys, traceback as tb, json, uuid
def print_exc(): print '*'*80; tb.print_exc(); print '*'*80
###
class AuthBase(object):
    def grant (_,u,p): return '',u,{}
    def revoke(_,t):   return
    def valid (_,t,g): return False
    def info  (_,t):   return '',{}
    pass
class MemAuth(AuthBase):
    def __init__(_):_.d=dict(
        t={},
        a={'app':{'uri':'http://localhost:8008/callback?at='}},
        u={'v~~vv':{'g':['user']},
           'u1~~' :{'g':['user']},
           'u2~~' :{'g':['user']},
           'v~':{},'u1~':{},'u2~':{},
           'user~' :{},'admin~':{}})
    def get(_,k,v=None):return _.d.get(k,v)
    def grant (_,username,password):
        tok,user = '',_.get('u').get(username+'~~'+password,{})
        if user:
            tok='t.'+str(uuid.uuid1())
            _.get('t')[tok]=(username,user)
            pass
        return tok,username,user
    def revoke(_,t):  return      _.get('t').pop(t,{})
    def valid (_,t,g):return g in _.get('t').get(t,('',{}))[1].get('g',[])
    def info  (_,t):  return      _.get('t').get(t,{})
    pass
_Auth=MemAuth()
def get_auth(): return _Auth
def set_auth(a): global _Auth; _Auth = a
###
def app(env, start_resp):
    def encode(x): return json.dumps(x) + '\n'
    from urlparse import parse_qs
    def reply(code,msg,body=None):
        start_resp(str(code)+' '+msg,headers)
        return [ body or str(code)+' '+msg ]
    headers=[('Content-Type', 'application/json'),
             ('Access-Control-Allow-Origin', '*')]
    path_info = env['PATH_INFO']
    # you can use / instead of ? and &
    if (  path_info.startswith('/auth/grant/') or
          path_info.startswith('/auth/valid/')  ):
        env['QUERY_STRING'] = path_info[12:].replace('/','&')
        path_info = env['PATH_INFO'] = path_info[:11]
        pass
    params = parse_qs(env['QUERY_STRING'])
    ###
    def grant():
        code,stat=200,'OK'
        u,p=params.get('u')[0],params.get('p')[0]
        tok,username,info = get_auth().grant(u,p)
        if not tok:  code,stat=401,'Unauthorized'
        return reply(code,stat,encode(
                dict(access_token=tok,
                     username=username,
                     authinfo=info)))
    def valid():
        t,g=params.get('t')[0],params.get('g')[0]
        if not get_auth().valid(t,g):
            return reply(401,'Unauthorized',encode({"result":False}))
        return reply(200,'OK',encode({"result":True}))
    def info():
        info = get_auth().info(params.get('t'))
        if not info:
            return reply(401,'Unauthorized',encode({}))
        return reply(200,'OK',[encode(dict(
                    result=dict(authinfo=info)))],encode({}))
    def revoke():
        get_auth().revoke(params.get('t')[0])
        return reply(200,'OK',encode({}))
    if path_info=='/auth/grant' : return grant ()
    if path_info=='/auth/valid' : return valid ()
    if path_info=='/auth/info'  : return info  ()
    if path_info=='/auth/revoke': return revoke()
    return reply(404,'Not Found',encode({}))
###
def glaunch(app,port,ssl_port):
    from gevent import spawn
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    server = WSGIServer(("0.0.0.0", port), app,
                        handler_class=WebSocketHandler)
    spawn(server.serve_forever)
    server = WSGIServer(("0.0.0.0", ssl_port), app,
                        keyfile='etc/server.key', certfile='etc/server.crt',
                        handler_class=WebSocketHandler)
    server.serve_forever()
    pass
if __name__=='__main__':glaunch(app,7080,7443)
