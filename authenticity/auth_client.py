import os, sys, traceback as tb, json, uuid, requests
_Urlbase =os.environ.get('CLIENT_URLBASE','s://localhost:7443')
def valid(t,g='user'):
    try:
        s='http%s/auth/valid?t=%s&g=%s'%(_Urlbase,t,g)
        req=requests.get(s, verify=False)
        return req.status_code==200
    except:
        print '*'*80
        tb.print_exc()
        print '*'*80
        return False
