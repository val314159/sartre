from prelude import *
from auth_core import get_auth
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
        print "QQQQQ", repr((t,g))
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
from common import glaunch
if __name__=='__main__':glaunch(app,7080,7443)
