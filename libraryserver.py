import json
import urllib


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        params = urllib.parse.parse_qs(parsed_path.query)
        service = path.strip(' /')

        if service in self.server.services:
            self.send_response(302)  # temporary redirect
            self.send_header('Location', self.server.services[service].get_url())
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        # parse post data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        # process signal data
        if 'signal' in data and data['signal'] in self.server.signals:
            response = self.server.signals.parse(data)

        # respond to signal
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = json.dumps(response)
        self.wfile.write( response_data.encode('utf-8') )


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    
    def __init__(self, server_address, RequestHandlerClass, services, signals):
        # pass services and signals objects to the request handler
        self.services = services
        self.signals = signals
        super().__init__(server_address, RequestHandlerClass)
