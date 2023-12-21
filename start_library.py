from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import os
import json
import time
import shelex
import urllib
import argparse
import platform
import subprocess

import services as _services
import signals as _signals


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global services
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        params = urllib.parse.parse_qs(parsed_path.query)
        service = path.strip(' /')

        if service in services:
            self.send_response(302)  # temporary redirect
            self.send_header('Location', services[service].get_url())
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        global signals
        # parse post data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        # process signal data
        if 'signal' in data and data['signal'] in signals:
            response = signals.parse(data)

        # respond to signal
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = json.dumps(response)
        self.wfile.write( response_data.encode('utf-8') )


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


if __name__ == '__main__':    
    program = 'python local_server.py'
    parser = argparse.ArgumentParser(prog=program, description='Offline library access via local HTTP server', epilog = help_epilog)
    parser.add_argument('-a', '--address', help='HTTP server address', default='')
    parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
    args = parser.parse_args()

    services = _services.Services()
    signals = _signals.Signals(services)
    services.add( _services.HTTPService(  services, 'landing',   args.address, args.port ) )
    services.add( _services.FilesService( services, 'files',     services.next_port()    ) )
    services.add( _services.KiwixService( services, 'reference', services.next_port()    ) )
    services.add( _services.KiwixService( services, 'forum',     services.next_port()    ) )
    
    services.start_all()
    #TODO launch browser to open landing page

    # run until all services are stopped
    try:
        print('Library services are available at {}'.format( services['landing'].get_url() ) )
        print('Press Ctrl+C to stop all services...')
        while True:
            if services.all_stopped:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        self._parent.stop_all()
    
