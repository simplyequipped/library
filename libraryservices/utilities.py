import os
import platform


def platform_info():
    # see https://download.kiwix.org/release/kiwix-tools/ to determine platform support
    # kiwix-tools platform support:
    #   windows-x86
    #   linux-x86
    #   linux-armhf (raspberry pi)
    #   linux-armv6
    #   linux-armv8
    #   linux-aarch64
    #   darmin-x86 (macos)
    #   darmin-arm (macos)
    
    _os = platform.system().lower()
    if _os not in ['windows', 'linux', 'darwin']:
        raise _osError('OS \'{}\' not supported, must be Windows, Linux, or Darwin (MacOS)'.format(OS))

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
        raise _osError('Architecture \'{}\' not supported'.format(machine))
    if _os == 'windows' and _arch not in ['x86']:
        raise _osError('Architecture \'{}\' not supported on Windows'.format(machine))
    elif _os == 'linux' and _arch not in ['x86', 'armhf', 'armv6', 'armv8', 'aarch64']:
        raise _osError('Architecture \'{}\' not supported on Linux'.format(machine))
    elif _os == 'darwin' and _arch not in ['x86', 'arm']:
        raise _osError('Architecture \'{}\' not supported on Darwin (MacOS)'.format(machine))

    return (_os, _arch, _bit)

def root_path():
    cwd = os.getcwd()

    if cwd.endswith('library'):
        return cwd
    elif cwd.endswith('libraryservices'):
        return os.path.abspath(os.path.join(cwd, '..'))
    else:
        raise OSError('Library services must be started from the directory containing the associated files.')

def kiwix_path():
    return os.path.join(root_path(), 'libraryservices/kiwix')

def kiwix_tools_path():
    global OS
    global ARCH

    tools_path = 'kiwix-tools-{}-{}'.format(OS, ARCH)
    return os.path.join(kiwix_path(), tools_path)

def kiwix_manage_path():
    global OS
    global ARCH

    manage_path = os.path.join(kiwix_tools_path(), 'kiwix-manage')

    if OS == 'windows':
        manage_path += '.exe'

    return manage_path

def kiwix_serve_path():
    global OS
    global ARCH

    serve_path = os.path.join(kiwix_tools_path(), 'kiwix-serve')

    if OS == 'windows':
        serve_path += '.exe'

    return serve_path

def kiwix_search_path():
    global OS
    global ARCH

    search_path = os.path.join(kiwix_tools_path(), 'kiwix-search')

    if OS == 'windows':
        search_path += '.exe'

    return search_path

def kiwix_library_path(service):
    library_path = 'library_{}.xml'.format(service)
    return os.path.join(kiwix_path(), library_path)

def kiwix_zim_path(service, make_dirs=True):
    zim_path = 'zim-{}'.format(service)
    zim_path = os.path.join(root_path(), zim_path)

    if not os.path.exists(zim_path) and make_dirs:
        os.makedirs(zim_path)

    return zim_path

def files_path():
    return os.path.join(root_path(), 'files')

def http_static_path():
    return os.path.join(root_path(), 'libraryservices/static')


# parse platform info on import
OS, ARCH, BIT = platform_info()

