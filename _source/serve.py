# local test server that behaves like Cloudflare Pages: extensionless URLs, _redirects, 404.html
import http.server, os, sys
ROOT=sys.argv[1]; PORT=int(sys.argv[2])
RED={}
for l in open(os.path.join(ROOT,'_redirects')):
    p=l.split()
    if len(p)>=2 and '*' not in p[0]: RED[p[0]]=p[1]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def log_message(s,*a): pass
    def do_GET(s):
        path=s.path.split('?')[0].split('#')[0]
        if path in RED: s.send_response(301); s.send_header('Location',RED[path]); s.end_headers(); return
        f=os.path.join(ROOT,path.lstrip('/'))
        if path.endswith('/') or os.path.isfile(f): return super().do_GET()
        if os.path.isfile(f+'.html'): s.path=path+'.html'; return super().do_GET()
        body=open(os.path.join(ROOT,'404.html'),'rb').read()
        s.send_response(404); s.send_header('Content-Type','text/html'); s.send_header('Content-Length',str(len(body))); s.end_headers(); s.wfile.write(body)
http.server.ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
