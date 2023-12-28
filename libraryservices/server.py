import os
import json
import urllib

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# local imports
import libraryservices


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.static_path = libraryservices.HTTP_STATIC_PATH
        super().__init__(*args, **kwargs)

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

            with open(os.path.join(self.static_path, 'index.html'), 'r') as f:
                index_html = f.read()

            # template variable handling
            index_html = index_html.replace('{port}', str(self.server.services['landing'].port) )
            content_size = '{:,.3f}'.format(self.server.services.content.total_size)
            index_html = index_html.replace('{content_size}', content_size)
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
        QUIT = False
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
                # stop HTTP service after other services
                if data['signal'] == 'quit':
                    QUIT = True

                response = self.server.signals.parse(data)
    
            # respond to signal
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = json.dumps(response)
            self.wfile.write( response_data.encode('utf-8') )

        if QUIT:
            self.server.services.stop_all()

    def log_message(self, format, *args):
        if self.server.services.debug:
            super().log_message(format, *args)



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    
    def __init__(self, server_address, RequestHandlerClass, services):
        self.services = services
        self.signals = libraryservices.Signals(self.services)
        super().__init__(server_address, RequestHandlerClass)

