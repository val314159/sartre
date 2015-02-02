from prelude import *

class PubSub:
    def __init__(_):
        from collections import defaultdict
        _.d = defaultdict(list)
        pass
    def pub(_,channel_name,message,skip=None):
        print "P BEFORE", repr(_.d), channel_name
        msg=json.dumps(dict(method='pub', params=[message]))
        print "BAH1 ", _.d[channel_name]
        for listener in _.d[channel_name]:
            print "BAH LOOP"
            if listener!=skip:
                print "NO SKIP", listener, skip
                listener.send(msg)
                pass
            else:
                print "SKIP", listener, skip
            pass
        print "P AFTER", repr(_.d), channel_name
        pass
    def _sub(_,channel_name,listener):
        lst=_.d[channel_name]
        if listener not in lst: lst.append(listener)        
        pass
    def _unsub(_,channel_name,listener):
        try:    _.d[channel_name].remove(listener)
        except: pass
        pass
    def sub(_,channel_names,listener):
        print "S BEFORE", repr(_.d)
        for ch in channel_names:
            unsub = ch.startswith('-')
            if unsub: _._unsub(ch[1:],listener)
            else:     _._sub(ch,listener)
            pass
        print "S AFTER", repr(_.d)
        pass
    pass
