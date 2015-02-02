from prelude import *

def DB(_=[]):
    from leveldb import LevelDB
    if not _: _.append(LevelDB('.db'))
    return _[0]

class db_obj:
    @staticmethod
    def db_create(ws,_id,rec):
        print  "DB CREATE", repr(rec)
        obj_id = obj.pop('id')
        DB().Put(obj_id+'.~meta', '{}')
        for k,v in obj.iteritems():
            DB().Put(obj_id+'.'+k, json.dumps(v))
            pass
        return "DB CREATE", repr(rec)
    @staticmethod
    def db_read(ws,_id,rec):
        print  "DB READ", repr(rec)
        for k,v in DB.RangeIter():
            print " == KV ", repr((k,v))
            pass
        return "DB READ", repr(rec)
    @staticmethod
    def db_update(ws,_id,rec):
        print  "DB UPDATE", repr(rec)
        obj_id=obj.pop('id')
        for k,v in obj.iteritems():
            print "----- UP", repr((k,v))
            DB().Put(obj_id+'.'+k, json.dumps(v))
            pass
        return "DB UPDATE"
    @staticmethod
    def db_delete(ws,_id,rec):
        print  "DB DELETE", repr(rec)
        DB().Delete(rec['id'])
        return "DB DELETE", repr(rec)
    pass

class pubsub_obj:
    from pubsub import PubSub
    PS = PubSub()
    @classmethod
    def sub(_,ws,_id,subs): return _.PS.sub(subs,ws)
    @classmethod
    def pub(_,ws,_id,ch,msg,skip=None): return _.PS.pub(ch,msg,skip)
    pass

class fs_obj:
    @staticmethod
    def load(ws,_id,path,off=0,sz=1024*1024):
        f=open(path)
        f.seek(int(off))
        data=f.read(sz)
        f.close()
        arr=path.split('/')
        ret=dict(
            dirname='/'.join(arr[:-1]),
            filename=arr[-1],
            data=data)
        print "RET", repr(ret)
        ws.send(json.dumps(dict(id=_id,
                method="load",
                result=ret)))
        return dict(
            dirname='/'.join(arr[:-1]),
            filename=arr[-1],
            data=data)
    @staticmethod
    def save(ws,_id,path,data,off=0,sz=None):
        f=open(path,'w')
        f.seek(int(off))
        f.write(data[:sz])
        f.close()
        ret=True
        print "RET", repr(ret)
        ws.send(json.dumps(dict(id=_id,
                method="load",
                result=ret)))
        return dict(result=True)
    @staticmethod
    def filesystem_walk(ws,_id,x):
        ret=dict((name,(dirs,files))
            for name,dirs,files in os.walk(x))
        print "RET", repr(ret)
        ws.send(json.dumps(dict(id=_id,
                method="filesystem_walk",
                result=ret)))
        return dict((name,(dirs,files))
                    for name,dirs,files in os.walk(x))
    pass

class fortune_obj:
    @staticmethod
    def fortune(ws,_id):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        print "YYY111", y
        ret = y[0]
        print "RET", repr(ret)
        ws.send(json.dumps(dict(id=_id,
                method="fortune",
                result=ret)))
        print "YYY999", y
        return y[0]
    motd = fortune
    pass

class obj(db_obj, pubsub_obj, fs_obj, fortune_obj):
    @staticmethod
    def ping(ws,_id,x=None): return ("PONG",x)
    pass

def dump_db():
    print "DUMP DB"
    for x in DB().RangeIter():
        print "X", x
