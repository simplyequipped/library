import time
import argparse
import webbrowser

# local imports
import services as srvcs

if __name__ == '__main__':    
    program = 'python start_library.py'
    parser = argparse.ArgumentParser(prog=program, description='Offline library services')
    parser.add_argument('-a', '--address', help='HTTP server address', default='')
    parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
    parser.add_argument('-d', '--debug', help='Enable debugging output', action='store_true')
    args = parser.parse_args()

    services = srvcs.Services()
    services.add( srvcs.HTTPService(  services, 'landing',   args.address, args.port ) )
    services.add( srvcs.FilesService( services, 'files',     services.next_port() ) )
    services.add( srvcs.KiwixService( services, 'reference', services.next_port() ) )
    services.add( srvcs.KiwixService( services, 'forum',     services.next_port() ) )
    
    services.debug = args.debug
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
        services.stop_all()
    
