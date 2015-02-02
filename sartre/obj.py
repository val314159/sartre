from prelude import *

def DB(_=[]):
    from leveldb import LevelDB
    if not _: _.append(LevelDB('.db'))
    return _[0]

class db_obj:
    @staticmethod
    def db_create(ws,_id,rec):
        print  "DB CREATE", repr(rec)
        obj_id = 'o.'+obj.pop('id')
        DB().Put(obj_id+'.', '{}')
        for k,v in obj.iteritems(): DB().Put(obj_id+'.'+k, json.dumps(v))
        ws.send(json.dumps(dict(id=_id,method="db_create",result=True)))
        return "DB CREATE", repr(rec)
    @staticmethod
    def db_read(ws,_id,rec={}):
        print  "DB READ", repr(rec)
        st,fi=('o.'+rec.get('start'),rec.get('finish','o.~~~'))
        for k,v in DB.RangeIter(st,fi):
            print " == KV ", repr((k,v))
            ws.send(json.dumps(dict(id=_id,method="db_read",result=(k,v))))
            pass
        ws.send(json.dumps(dict(id=_id,method="db_read",result=True)))
        return "DB READ", repr(rec)
    @staticmethod
    def db_update(ws,_id,rec):
        print  "DB UPDATE", repr(rec)
        obj_id=obj.pop('id')
        for k,v in obj.iteritems():
            print "----- UP", repr((k,v))
            DB().Put(obj_id+'.'+k, json.dumps(v))
            pass
        ws.send(json.dumps(dict(id=_id,method="db_update",result=True)))
        return "DB UPDATE"
    @staticmethod
    def db_delete(ws,_id,rec):
        print  "DB DELETE", repr(rec)
        DB().Delete(rec['id'])
        ws.send(json.dumps(dict(id=_id,method="db_delete",result=True)))
        return "DB DELETE", repr(rec)
    pass

class pubsub_obj:
    from pubsub import PubSub
    PS = PubSub()
    @classmethod
    def sub(_,ws,_id,subs):
        ret=_.PS.sub(subs,ws)
        ws.send(json.dumps(dict(id=_id,method="sub",result=ret)))
        return ret
    @classmethod
    def pub(_,ws,_id,ch,msg,skip=None):
        print "PUBBBBBB", repr((ws,_id,ch,msg,skip))
        ret=_.PS.pub(ch,msg,skip)
        ws.send(json.dumps(dict(id=_id,method="pub",result=ret)))
        return ret
    pass

class fs_obj:
    @staticmethod
    def fs_load(ws,_id,path,off=0,sz=1024*1024):
        f=open(path)
        f.seek(int(off))
        data=f.read(sz)
        f.close()
        arr=path.split('/')
        ret=dict(dirname='/'.join(arr[:-1]),filename=arr[-1],data=data)
        ws.send(json.dumps(dict(id=_id,method="fs_load",result=ret)))
        return dict(dirname='/'.join(arr[:-1]),filename=arr[-1],data=data)
    @staticmethod
    def fs_save(ws,_id,path,data,off=0,sz=None):
        f=open(path,'w')
        f.seek(int(off))
        f.write(data[:sz])
        f.close()
        ws.send(json.dumps(dict(id=_id,method="fs_save",result=True)))
        return dict(result=True)
    @staticmethod
    def fs_walk(ws,_id,x):
        ret=dict((name,(dirs,files)) for name,dirs,files in os.walk(x))
        ws.send(json.dumps(dict(id=_id,method="fs_walk",result=ret)))
        return dict((name,(dirs,files)) for name,dirs,files in os.walk(x))
    pass

class fortune_obj:
    @staticmethod
    def fortune(ws,_id):
        import subprocess
        x=subprocess.Popen(['fortune'],stdout=subprocess.PIPE)
        y = x.communicate()
        ret = y[0]
        ws.send(json.dumps(dict(id=_id,method="fortune",result=ret)))
        return y[0]
    motd = fortune
    pass

class obj(db_obj, pubsub_obj, fs_obj, fortune_obj):
    @staticmethod
    def ping(ws,_id,x=None):
        ws.send(json.dumps(dict(id=_id,method="ping",result=("PONG",x))))
        return ("PONG",x)
    pass

def dump_db():
    print "DUMP DB"
    for x in DB().RangeIter():
        print "X", x
