from prelude import *
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
        print "QQQQ", repr((username,password))
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
def set_auth(a):    global _Auth;    _Auth = a
