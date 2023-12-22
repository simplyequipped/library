import time
import argparse
import webbrowser

# local imports
import services as srvcs


#TODO
# - handle ports in index.html (hrefs and ajax)


if __name__ == '__main__':    
    program = 'python start_library.py'
    parser = argparse.ArgumentParser(prog=program, description='Offline library access via local HTTP server', epilog = help_epilog)
    parser.add_argument('-a', '--address', help='HTTP server address', default='')
    parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
    args = parser.parse_args()

    services = srvcs.Services()
    services.add( srvcs.HTTPService(  services, 'landing',   args.address, args.port ) )
    services.add( srvcs.FilesService( services, 'files',     services.next_port() ) )
    services.add( srvcs.KiwixService( services, 'reference', services.next_port() ) )
    services.add( srvcs.KiwixService( services, 'forum',     services.next_port() ) )
    
    services.start_all()
    webbrowser.open( services['landing'].url() )

    # run until all services are stopped
    try:
        print('Library services are available at {}'.format( services['landing'].url() ) )
        print('Press Ctrl+C to stop all services...')
        while True:
            if services.all_stopped:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        self.services.stop_all()
    
