from gevent import monkey;monkey.patch_all()
import os, sys, traceback as tb, json, uuid

def print_exc():
    print '*'*80
    tb.print_exc()
    print '*'*80
    pass
