from prelude import *

def DB(_=[]):
    from leveldb import LevelDB
    if not _: _.append(LevelDB('.db'))
    return _[0]

class PS:
    def __init__(_):
        from collection import default_dict
        _.d = default_dict(list)
        pass
    def pub(_,channel_name,message,skip=None):
        lst=_.d[channel_name]
        for listener in _.d[channel_name]:
            if listener!=skip:
                listener.msg(channel_name,message)
                pass
            pass
        pass
    def sub(_,channel_name,listener):
        lst=_.d[channel_name]
        if channel_name not in lst:
            lst.append(listener)
            pass
        pass
    def unsub(_,channel_name,listener):
        lst=_.d[channel_name]
        if channel_name in lst:
            lst.remove(listener)
            pass
        pass
    pass
_PS=PS()

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
    def sub(subs):
        for ch in subs:
            if ch.startswith('-'):
                _PS.unsub(ch[1:])
            else:
                _PS.sub(ch)
                pass

    @staticmethod
    def pub(ch,msg,skip=None):
        _PS.pub(ch,msg,skip)
        return "PUB"

    @staticmethod
    def ping(*a,**kw):
        return "PONG", repr((a,kw))
    @staticmethod
    def load(ws,path, offset=0,size=-1):
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
    def save(ws,filename, data, offset=0,size=-1):
        f=open(filename,'w')
        f.write(data)
        f.close()
        return dict(result=True)

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
    @staticmethod
    def motd(ws):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        return y[0]
    pass

def dump_db():
    print "DUMP DB"
    for x in DB().RangeIter():
        print "X", x
