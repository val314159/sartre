from prelude import *

class PubSub:
    def __init__(_):
        from collections import defaultdict
        _.d = defaultdict(list)
        pass
    def pub(_,channel_name,message,skip=None):
        msg=json.dumps(dict(method='pub', params=[message]))
        for listener in _.d[channel_name]:
            if listener!=skip: listener.send(msg)
            pass
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
        for ch in channel_names:
            unsub = ch.startswith('-')
            if unsub: _._unsub(ch[1:],listener)
            else:     _._sub(ch,listener)
            pass
        pass
    pass
