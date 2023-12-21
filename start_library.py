import time
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# local imports
import services as _services
import signals as _signals


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
    
