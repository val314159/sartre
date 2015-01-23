from prelude import *

def valid(t,g='user'):
    try:
        import requests
        xbase ='s://localhost:9443'
        #xbase = '://localhost:9080'
        s='http%s/auth/valid?t=%s&g=%s'%(xbase,t,g)
        req=requests.get(s, verify=False)
        print "GOOD"
        return req.status_code==200
    except:
        print "BAD"
        print_exc()
        return False
