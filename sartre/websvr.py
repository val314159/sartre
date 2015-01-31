from prelude import *
from bottle import request, response, default_app, abort, static_file, redirect
from common import authorize_token

app = default_app()

@app.route('/')
def index():
    return redirect('/static/index.html')

@app.route('/test')
def test():
    response.headers['Access-Control-Allow-Origin'] = '*'
    tok = authorize_token(None)
    return ['ok']

import websock

@app.route('/websocket')
def handle_websocket():
    response.headers['Access-Control-Allow-Origin'] = '*'
    tok = authorize_token()
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        raise abort(400, 'Expected WebSocket request.')
    websock.process(tok, wsock)

@app.route('/README.md')
@app.route('/static/<filename:path>')
def serve_static(filename=None):
    from markdown2 import markdown_path
    if filename is None  or  filename.endswith('.md'):
        response.headers['Access-Control-Allow-Origin'] = '*'
        filename = 'static/'+filename if filename else 'README.md'
        print "static", filename
        return markdown_path(filename)
    resp = static_file(filename, root='static/')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__=='__main__':
    from common import glaunch
    from obj import dump_db
    print 'DB0', '='*80
    dump_db()
    print 'DB9', '='*80
    glaunch(app,8080,8443)
