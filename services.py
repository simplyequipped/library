import os
import sys
import shlex
import socket
import platform
import threading
import subprocess

# local imports
import tools
import zimlibrary
from libraryserver import ThreadedHTTPServer, LibraryRequestHandler


class Service:
    # service types
    KIWIX = 'kiwix'
    FILES = 'files'
    HTTP  = 'http'
    
    def __init__(self, parent, name, port=None):
        self.name = name
        self.port = port
        self.running = False
        self.type = None
        self.parent = parent
        self._process = None
        self._process_cmd = None
        self._process_shell = True
        self._socket_timeout = 2 # seconds

    def start(self):
        if self.running or self._process_cmd is None:
            return

        if self._process_shell:
            # if shell=True, use arg string
            cmd = self._process_cmd
        else:
            # if shell=False, use arg list
            cmd = shlex.split(self._process_cmd)
    
        if self.parent.debug:
            self._process = subprocess.Popen(cmd, shell=self._process_shell)
        else:
            self._process = subprocess.Popen(cmd, shell=self._process_shell, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

    def url(self):
        return 'http://localhost:{}/'.format(self.port)

    def active(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._socket_timeout)
                sock.connect( ('localhost', self.port) )
            self.running = True
        except (socket.timeout, ConnectionRefusedError):
            self.running = False

        return self.running


class KiwixService (Service):
    def __init__(self, parent, name, port=None):
        super().__init__(parent, name, port)
        self.type = Service.KIWIX
        self.library = zimlibrary.Library(self.name)
        # rebuild zim library, ensures correct path separators for current platform
        self.library.build()
        
    def start(self):
        # windows example: start /b D:\kiwix\kiwix-tools-windows-x86\kiwix-serve.exe --port 8001 --library D:\kiwix\library_reference.xml
        self._process_cmd = '{} --port {} --library {}'.format(tools.kiwix_serve_path(), self.port, self.library.path)
        super().start()


class FilesService (Service):
    def __init__(self, parent, name, port=None):
        super().__init__(parent, name, port)
        self.type = Service.FILES
        
    def start(self):
        # example: python -m http.server 8003 --directory /mnt/ext/files
        self._process_cmd = '{} -m http.server {} --directory {}'.format(sys.executable, self.port, tools.files_path())
        super().start()


class HTTPService (Service):
    def __init__(self, parent, name, address=None, port=None):
        super().__init__(parent, name, port)
        self.type = Service.HTTP
        self.address = address
        self.server = None

    def start(self):
        server_address = (self.address, self.port)

        # pass reference to services
        self.server = ThreadedHTTPServer(server_address, LibraryRequestHandler, self.parent)

        # non-blocking server loop
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()

        self.running = True

    def stop(self):
        self.server.server_close()
        self.running = False


class Services:
    def __init__(self):
        self._services = {}
        self.all_stopped = False
        self.debug = False
        
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
        ports = [service.port for service in self._services.values()]

        if len(ports) == 0:
            return None
        
        return max(ports) + 1

