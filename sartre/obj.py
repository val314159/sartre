from prelude import *

def DB(_=[]):
    from leveldb import LevelDB
    if not _: _.append(LevelDB('.db'))
    return _[0]

class db_obj:
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
        for k,v in DB.RangeIter():
            print " == KV ", repr((k,v))
            pass
        return "DB READ", repr(rec)
    @staticmethod
    def db_update(ws,rec):
        print  "DB UPDATE", repr(rec)
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
    pass

class pubsub_obj:
    from pubsub import PubSub
    PS = PubSub()
    @classmethod
    def sub(_,ws,subs): return _.PS.sub(subs,ws)
    @classmethod
    def pub(_,ws,ch,msg,skip=None): return _.PS.pub(ch,msg,skip)
    pass

class fs_obj:
    @staticmethod
    def load(ws,path,off=0,sz=None):
        f=open(path)
        f.seek(int(offset))
        data=f.read(size)
        f.close()
        arr=path.split('/')
        return dict(
            dirname='/'.join(arr[:-1]),
            filename=arr[-1],
            data=data)
    @staticmethod
    def save(ws,path,data,off=0,sz=None):
        f=open(path,'w')
        f.seek(int(offset))
        f.write(data[:size])
        f.close()
        return dict(result=True)
    @staticmethod
    def filesystem_walk(ws,x):
        return dict((name,(dirs,files))
                    for name,dirs,files in os.walk(x))
    pass

class fortune_obj:
    @staticmethod
    def fortune(ws):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        return y[0]
    motd = fortune
    pass

class obj(db_obj, pubsub_obj, fs_obj, fortune_obj):
    @staticmethod
    def ping(x=None): return ("PONG",x)
    pass

def dump_db():
    print "DUMP DB"
    for x in DB().RangeIter():
        print "X", x
