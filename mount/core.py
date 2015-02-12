import logging

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

if not hasattr(__builtins__, 'bytes'):
    bytes = str

class Memory(LoggingMixIn, Operations):
    def __init__(self):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        self.mkdir(u'/',0755)

    def _mkfil(self, path, typ, mode, nlink=1, sz=0):
        self.files[path]=dict(st_mode=(typ|mode),st_nlink=nlink, st_size=sz,
                              st_ctime=time(),st_mtime=time(),st_atime=time())
        pass
    ###
    def getxattr(self, path, name, position=0):
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR
    def listxattr(self, path):
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()
    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})
        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR
    def setxattr(self, path, name, value, options, position=0):
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value
    ###
    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(ENOENT)
        return self.files[path]
    def read(self, path, size, offset, fh):
        return self.data[path][offset:offset + size]
    def readdir(self, path, fh):
        if path=='/': path=''
        return ['.','..']+[
            x[1+len(path):] for x in self.files
            if (x!='/' and x.startswith(path+'/') and 
                x.find('/',1+len(path))==-1)]
    def readlink(self, path):
        return self.data[path]
    ###
    def chmod(self, path, mode):
        self.files[path]['st_mode'] &= 0770000
        self.files[path]['st_mode'] |= mode
    def chown(self, path, uid, gid):
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid
    def create(self, path, mode):
        self._mkfil(path,S_IFREG,mode)
        self.fd += 1
        return self.fd
    def mkdir(self, path, mode):
        self._mkfil(path,S_IFDIR,mode,nlink=2)
        self.files[u'/']['st_nlink'] += 1
    def open(self, path, flags):
        self.fd += 1
        return self.fd
    def rename(self, old, new):
        self.files[new] = self.files.pop(old)
    def rmdir(self, path):
        self.files.pop(path)
        self.files[u'/']['st_nlink'] -= 1
    def symlink(self, target, source):
        self._mkfil(target,S_IFREG,mode,sz=len(source))
        self.data[target] = source
    def truncate(self, path, length, fh=None):
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length
    def unlink(self, path):
        self.files.pop(path)
    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
    def write(self, path, data, offset, fh):
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)

def main(cls=Memory):
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.getLogger().setLevel(logging.DEBUG)
    fuse = FUSE(cls(), argv[1], foreground=True)

if __name__=='__main__':main()
