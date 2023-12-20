from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import os
import urllib
import argparse
import platform
import threading
import subprocess


class MyRequestHandler(BaseHTTPRequestHandler):
    connections = set()

    def do_GET(self):
        global kiwix_libraries
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        params = urllib.parse.parse_qs(parsed_path.query)

        if path in ['/kiwix/{}'.format(library) for library in kiwix_libraries]:
            library = path.split('/')[-1]
            run_kiwix_serve(library)
            
            self.send_response(302)  # temporary redirect
            self.send_header('Location', 'http://example.com/new_location')
            self.end_headers()
            self.connections.add(self.client_address)

        elif path == '/files':
            if 'param' in params:
                param_value = params['param'][0]
                result = custom_function(param_value)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(result).encode())
                self.connections.add(self.client_address)

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def finish(self):
        super().finish()
        self.connections.remove(self.client_address)
        if not self.connections:
            print("Last client disconnected. Stopping the server.")
            self.server.shutdown()
            stop_running_services()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def run_kiwix_serve(library):
    global running_services
    global service_ports

    if library in running_services:
        return

    _os, _arch, _bit = get_platform_info()
    kiwix_serve_path = os.path.join( os.getcwd(), get_kiwix_serve_path() )
    kiwix_library_path = os.path.join( os.getcwd(), 'kiwix/library_{}.xml'.format(library) )

    if _os == 'windows':
        prefix = 'start /b ' # note trailing space
    if _os == 'linux':
        prefix = ''
    if _os == 'darwin':
        prefix = ''

    cmd = '{}{} --port {} --library {}'.format(prefix, kiwix_serve_path, service_ports[library], kiwix_library_path)
    
    thread = threading.Thread(target=start_subprocess_thread, args=(cmd,))
    thread.daemon = True
    thread.start()

def run_file_browser():
    global service_ports
    
    files_path = os.path.join( os.getcwd(), 'files' )
    #TODO handle python vs python3
    cmd = 'python -m http.server {} --directory {}'.format(service_ports['files'], files_path)
    thread = threading.Thread(target=start_subprocess_thread, args=(cmd,))
    thread.daemon = True
    thread.start()

#TODO
def stop_running_services():
    global running_services

def get_platform_info():
    # see https://download.kiwix.org/release/kiwix-tools/ to determine platform support
    # kiwix-tools platform support as of Dec 20, 2023:
    #
    # windows-x86
    # linux-x86
    # linux-armhf (raspberry pi)
    # linux-armv6
    # linux-armv8
    # darmin-x86 (macos)
    # darmin-arm (macos)
    
    _os = platform.system().lower
    if _os not in ['windows', 'linux', 'darwin']:
        raise OSError('OS \'{}\' not supported, must be Windows, Linux, or Darwin (MacOS)'.format(_os))

    machine = platform.machine().lower()
    if 'arm' in machine:
        _arch = 'arm'

        # get arm version
        if 'v' in machine:
            _arch += 'v'
            _arch += machine.split('v')[1][0] # 'armv71' -> ['arm', '71'] -> '71' -> '7'

         # check if raspberry pi
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
            with open('/sys/firmware/devicetree/base/model', 'r') as f:
                model = f.read()
                if 'Raspberry Pi' in model:
                    _arch = 'armhf'
            
    elif '64' in machine:
        if '86' in machine or 'AMD' in machine:
            _arch = 'x86'
        else:
            _arch = None
    else:
        _arch = 'x86'

    _bit = platform.architecture()[0].replace('bit', '')

    if _arch is None:
        raise OSError('Architecture \'{}\' not supported'.format(machine))
    if _os == 'windows' and _arch not in ['x86']:
        raise OSError('Architecture \'{}\' not supported on Windows'.format(machine))
    elif _os == 'linux' and _arch not in ['x86', 'armhf', 'armv6', 'armv8']:
        raise OSError('Architecture \'{}\' not supported on Linux'.format(machine))
    elif _os == 'darwin' and _arch not in ['x86', 'arm']:
        raise OSError('Architecture \'{}\' not supported on Darwin (MacOS)'.format(machine))

    return (_os, _arch, _bit)

def get_kiwix_serve_path():
    # kiwix-tools directories as of Dec 20, 2023:
    #
    # kiwix/kiwix-tools-windows-x86/
    # kiwix/kiwix-tools-linux-x86/
    # kiwix/kiwix-tools-linux-armhf/
    # kiwix/kiwix-tools-linux-armv6/
    # kiwix/kiwix-tools-linux-armv8/
    # kiwix/kiwix-tools-darmin-x86/
    # kiwix/kiwix-tools-darmin-arm/
    _os, _arch, _bit = get_platform_info()
    path = 'kiwix/kiwix-tools-{}-{}/kiwix-serve'.format(_os, _arch)
    
    if _os == 'windows':
        path += '.exe'

    return path

#TODO
def start_subprocess_thread(kiwix_tools_path):
    subprocess.run()



if __name__ == '__main__':
    kiwix_libraries = ['reference', 'forum']
    services = kiwix_libraries + ['files']
    running_services = []
    service_ports = {}
    
    program = 'python local_server.py'
    parser = argparse.ArgumentParser(prog=program, description='Offline library access via local HTTP server', epilog = help_epilog)
    parser.add_argument('-a', '--address', help='HTTP server address', default='')
    parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
    args = parser.parse_args()

    # set network port numbers for each service, incremented from designated port
    next_port = args.port + 1
    for service in services:
        service_ports[service] = next_port
        next_port += 1
    
    server_address = (args.address, args.port)
    httpd = ThreadedHTTPServer(server_address, MyRequestHandler)
    print('Server is running and will stop automatically once the last client disconnects')
    print('Press Ctrl-C to stop the server manually')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()




