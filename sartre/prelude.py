from gevent import monkey;monkey.patch_all()
from geventwebsocket import WebSocketError
import os, sys, traceback as tb, json, uuid
from pprint import pprint

def print_exc():
    print '*'*80
    tb.print_exc()
    print '*'*80
    pass
