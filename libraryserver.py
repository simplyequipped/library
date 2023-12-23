import json
import urllib

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# local imports
import signals


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse request path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        params = urllib.parse.parse_qs(parsed_path.query)
        service = path.strip(' /')

        if path == '/':
            # library landing html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('static/index.html', 'r') as f:
                index_html = f.read()

            # template variable handling
            index_html = index_html.replace( '{port}', str(self.server.services['landing'].port) )
            self.wfile.write( index_html.encode('utf-8') )
            
        elif service in self.server.services:
            self.send_response(302)  # temporary redirect
            self.send_header( 'Location', self.server.services[service].url() )
            self.end_headers()
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        # parse request path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        # parse post data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if path == '/signals':
            # process signal data
            if 'signal' in data and data['signal'] in self.server.signals:
                response = self.server.signals.parse(data)
    
            # respond to signal
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = json.dumps(response)
            self.wfile.write( response_data.encode('utf-8') )

    def log_message(self, format, *args):
        if self.server.services.debug:
            super().log_message(format, *args)



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    
    def __init__(self, server_address, RequestHandlerClass, services):
        self.services = services
        self.signals = signals.Signals(self.services)
        super().__init__(server_address, RequestHandlerClass)

