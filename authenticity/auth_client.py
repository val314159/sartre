from prelude import *

def valid(t,g='user'):
    try:
        import requests
        xbase ='s://localhost:7443'
        #xbase = '://localhost:7080'
        s='http%s/auth/valid?t=%s&g=%s'%(xbase,t,g)
        req=requests.get(s, verify=False)
        return req.status_code==200
    except:
        print_exc()
        return False
