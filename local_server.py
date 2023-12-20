from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import os
import time
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
            #TODO test delay to make sure service is running, including on slow platforms like raspberry pi
            time.sleep(2)
            # redirect to service url
            self.send_response(302)  # temporary redirect
            self.send_header('Location', get_service_url(library))
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


def run_kiwix_libraries():
    global kiwix_libraries

    for library in kiwix_libraries:
        run_kiwix_serve(library)

def run_kiwix_serve(library):
    global running_services
    global service_ports

    if library in running_services:
        return

    _os, _arch, _bit = get_platform_info()
    kiwix_serve_path = get_kiwix_serve_path()
    kiwix_library_path = get_kiwix_library_path(library)

    if _os == 'windows':
        prefix = 'start /b ' # note trailing space
    if _os == 'linux':
        prefix = ''
    if _os == 'darwin':
        prefix = ''

    # windows example: start /b D:\kiwix\kiwix-tools-windows-x86\kiwix-serve.exe --port 8001 --library D:\kiwix\library_reference.xml
    cmd = '{}{} --port {} --library {}'.format(prefix, kiwix_serve_path, service_ports[library], kiwix_library_path)
    
    thread = threading.Thread(target=start_subprocess_thread, args=(cmd,))
    thread.daemon = True
    thread.start()

    running_services.append(library)

def run_file_browser():
    global service_ports
    
    files_path = os.path.join( os.getcwd(), 'files' )
    # example: python -m http.server 8003 --directory /mnt/ext/files
    cmd = '{} -m http.server {} --directory {}'.format(get_python_cmd(), service_ports['files'], files_path)
    thread = threading.Thread(target=start_subprocess_thread, args=(cmd,))
    thread.daemon = True
    thread.start()

#TODO
def stop_running_services():
    global running_services

def get_python_cmd():
    try:
        version = int(subprocess.check_output(['python', '--version'], text=True).split(' ')[1].split('.')[0]) # 'Python 3.9.5' -> ['Python', '3.9.5'] -> ['3', '9', '5'] -> 3
    except:
        return 'python3'

    if version == 3:
        return 'python'
    else:
        return 'python3'

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

def get_kiwix_library_path(library):
    return os.path.join( os.getcwd(), 'kiwix/library_{}.xml'.format(library) )

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

    return os.path.join(os.getcwd(), path)

def get_service_url(service):
    global services
    global service_ports
    global running_services

    if service not in services:
        raise ValueError('Service \'{}\' unknown'.format(service))
    elif service not in running_services:
        service = 'landing'

    return 'http://localhost/:{}'.format(service_ports[service])

#TODO
def start_subprocess_thread(kiwix_tools_path):
    subprocess.run()



if __name__ == '__main__':
    kiwix_libraries = ['reference', 'forum']
    services = kiwix_libraries + ['landing', 'files']
    running_services = []
    
    program = 'python local_server.py'
    parser = argparse.ArgumentParser(prog=program, description='Offline library access via local HTTP server', epilog = help_epilog)
    parser.add_argument('-a', '--address', help='HTTP server address', default='')
    parser.add_argument('-p', '--port', help='HTTP server port', default=8000, type=int)
    args = parser.parse_args()

    # store network port for landing page
    service_ports['landing'] = args.port
    # store network ports for other services, incremented from landing page port
    next_port = args.port + 1
    for service in services:
        if service in service_ports:
            continue
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




