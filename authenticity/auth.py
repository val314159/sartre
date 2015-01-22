import os, sys, json, traceback as tb, uuid, requests
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
        print "return", tok,username,user
        return tok,username,user
    def revoke(_,t):  return      _.get('t').pop(t,{})
    def valid (_,t,g):
        print '-'*80
        print              t
        print       _.get('t')
        print       _.get('t').get(t,('',{}))
        print       _.get('t').get(t,('',{}))[1]
        print       _.get('t').get(t,('',{}))[1].get('g',[])
        print  g in _.get('t').get(t,('',{}))[1].get('g',[])
        return g in _.get('t').get(t,('',{}))[1].get('g',[])
    def info  (_,t):  return      _.get('t').get(t,{})
    pass
_Auth=MemAuth()
def get_auth(): return _Auth
def set_auth(a):
    global _Auth
    _Auth = a
    pass
from bottle import request, response, redirect, default_app, abort
app=default_app()
@app.route('/auth/grant')
def auth_grant():
    response.headers['Access-Control-Allow-Origin'] = '*'
    rp=request.params
    tok,username,info = get_auth().grant(rp.get('u'),rp.get('p'))
    if not tok: response.status=401
    return dict(result=dict(access_token=tok,username=username,authinfo=info))
@app.route('/auth/valid')
def auth_valid():
    response.headers['Access-Control-Allow-Origin'] = '*'
    rp=request.params
    if not get_auth().valid(rp['t'],rp['g']): response.status=401
    return ['']
@app.route('/auth/info')
def auth_info():
    response.headers['Access-Control-Allow-Origin'] = '*'
    info = get_auth().info(request.params.get('t'))
    if not info: response.status=401
    return dict(result=info)
@app.route('/auth/revoke')
def auth_revoke():
    response.headers['Access-Control-Allow-Origin'] = '*'
    info = get_auth().revoke(request.params.get('t'))
    if not info: response.status=401
    return dict(result=info)

from gevent import spawn
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 9080), app,
                    handler_class=WebSocketHandler)
spawn(server.serve_forever)
server = WSGIServer(("0.0.0.0", 9443), app,
                    keyfile='etc/server.key', certfile='etc/server.crt',
                    handler_class=WebSocketHandler)
server.serve_forever()
