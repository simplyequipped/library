import os
import sys
import shlex
import socket
import platform
import threading
import subprocess

# local imports
from libraryserver import ThreadedHTTPServer, LibraryRequestHandler


class Service:
    # service types
    KIWIX = 'kiwix'
    FILES = 'files'
    HTTP  = 'http'
    
    def __init__(self, parent, name, port=None):
        self.name = name
        self.running = False
        self._type = None
        self._parent = parent
        self._process = None
        self._process_cmd = None
        self._process_shell = True
        self._root_path = os.getcwd()
        self._socket_timeout = 2 # seconds

        _os, _arch, _bit = self._get_platform_info()
        self._platform = {
            'os': _os,
            'arch': _arch,
            'bit': _bit
        }

        if port is not None:
            self.set_port(port)
        else:
            self._port = None

    def start(self):
        if self.running or self._process_cmd is None:
            return

        if self._process_shell:
            # if shell=True, use arg string
            cmd = self._process_cmd
        else:
            # if shell=False, use arg list
            cmd = shlex.split(self._process_cmd)
    
        self._process = subprocess.Popen(cmd, shell=self._process_shell)
        self.running = True

    def stop(self):
        if self._process is None:
            return

        self._process.terminate()

        try:
            self._process.wait(timeout = 2)
        except subprocess.TimeoutExpired:
            self._process.kill()

        self.running = False

    def port(self):
        return self._port

    def set_port(self, port):
        self._port = port

    def url(self):
        return 'http://localhost:{}/'.format(self._port)

    def active(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._socket_timeout)
                sock.connect( (host, port) )
            self.running = True
        except (socket.timeout, ConnectionRefusedError):
            self.running = False

        return self.running

    def _get_cmd_prefix(self):
        if self._platform['os'] == 'windows':
            return 'start /b'
        elif self._platform['os'] == 'linux':
            return ''
        elif self._platform['os'] == 'darwin':
            return ''
        else:
            return ''

    def _get_platform_info(self):
        # see https://download.kiwix.org/release/kiwix-tools/ to determine platform support
        # kiwix-tools platform support as of Dec 20, 2023:
        #
        # windows-x86
        # linux-x86
        # linux-armhf (raspberry pi)
        # linux-armv6
        # linux-armv8
        # linux-aarch64
        # darmin-x86 (macos)
        # darmin-arm (macos)
        
        _os = platform.system().lower()
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

        elif 'aarch64' in machine:
            _arch = 'aarch64'

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
        elif _os == 'linux' and _arch not in ['x86', 'armhf', 'armv6', 'armv8', 'aarch64']:
            raise OSError('Architecture \'{}\' not supported on Linux'.format(machine))
        elif _os == 'darwin' and _arch not in ['x86', 'arm']:
            raise OSError('Architecture \'{}\' not supported on Darwin (MacOS)'.format(machine))
    
        return (_os, _arch, _bit)


class KiwixService (Service):
    def __init__(self, parent, name, port=None):
        super().__init__(parent, name, port)
        self._type = Service.KIWIX
        self._kiwix_path = os.path.join( self._root_path, 'kiwix')
        self._library_path = os.path.join( self._kiwix_path, 'library_{}.xml'.format(self.name) )

        self._kiwix_serve_path = 'kiwix-tools-{}-{}/kiwix-serve'.format( self._platform['os'], self._platform['arch'] )
        if self._platform['os'] == 'windows':
            self._kiwix_serve_path += '.exe'
        self._kiwix_serve_path = os.path.join( self._kiwix_path, self._kiwix_serve_path )
        
    def start(self):
        # windows example: start /b D:\kiwix\kiwix-tools-windows-x86\kiwix-serve.exe --port 8001 --library D:\kiwix\library_reference.xml
        self._process_cmd = '{} {} --port {} --library {}'.format(self._get_cmd_prefix(), self._kiwix_serve_path, self._port, self._library_path).strip()
        super().start()


class FilesService (Service):
    def __init__(self, parent, name, port=None):
        super().__init__(parent, name, port)
        self._type = Service.FILES
        self._files_path = os.path.join( self._root_path, 'files' )
        
    def start(self):
        # example: python -m http.server 8003 --directory /mnt/ext/files
        self._process_cmd = '{} -m http.server {} --directory {}'.format(sys.executable, self._port, self._files_path)
        super().start()


class HTTPService (Service):
    def __init__(self, parent, name, address=None, port=None):
        super().__init__(parent, name, port)
        self._type = Service.HTTP
        self._address = address
        self._server = None

    def address(self):
        return self._address
    
    def set_address(self, address):
        self._address = address
        
    def start(self):
        server_address = (self._address, self._port)

        # pass reference to services
        self._server = ThreadedHTTPServer(server_address, LibraryRequestHandler, self._parent)

        # non-blocking server loop
        thread = threading.Thread(target=self._server.serve_forever)
        thread.daemon = True
        thread.start()

        self.running = True

    def stop(self):
        self._server.server_close()
        self.running = False


class Services:
    def __init__(self):
        self._services = {}
        self.all_stopped = False
        
    def __getitem__(self, name):
        return self._services[name]

    def __setitem__(self, name, service):
        self._services[name] = service

    def __delitem__(self, name):
        del self._services[name]

    def __len__(self):
        return len(self._services)

    def __iter__(self):
        return iter(self._services)

    def __contains__(self, name):
        return name in self._services

    def keys(self):
        return list(self._services.keys())

    def values(self):
        return list(self._services.values())

    def items(self):
        return list(self._services.items())

    def add(self, service):
        self._services[service.name] = service

    def start_all(self):
        for service in self._services.values():
            service.start()

    def stop_all(self):
        for service in self._services.values():
            service.stop()

        self.all_stopped = True

    def next_port(self):
        ports = [service.port() for service in self._services.values()]

        if len(ports) == 0:
            return None
        
        return max(ports) + 1
