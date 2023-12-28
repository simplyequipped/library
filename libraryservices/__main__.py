import os
import time
import argparse
import webbrowser

# local imports
import libraryservices

program = 'python start_library.py'
parser = argparse.ArgumentParser(prog=program, description='Offline library services')
parser.add_argument('-a', '--address', help='HTTP server address', default='')
parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
parser.add_argument('-d', '--debug', help='Enable debugging output', action='store_true')
parser.add_argument('-c', '--csv', help='CSV file of content to download', default=None)
args = parser.parse_args()

services = libraryservices.Services()
services.add( libraryservices.HTTPService(  services, 'landing',   args.address, args.port ) )
services.add( libraryservices.FilesService( services, 'files',     services.next_port() ) )
services.add( libraryservices.KiwixService( services, 'reference', services.next_port() ) )
services.add( libraryservices.KiwixService( services, 'forum',     services.next_port() ) )

if args.csv is None:
    args.csv = os.path.join(libraryservices.ROOT_PATH, 'recommended_content.csv')
else:
    args.csv = os.path.abspath(args.csv)

services.debug = args.debug
services.content.set_csv_file(args.csv)
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

