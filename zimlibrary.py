import os
import subprocess

# local imports
import tools


class Library:
    def __init__(self, service):
        self.service = service
        self.path = tools.kiwix_library_path(self.service)
        self.zim_path = tools.kiwix_zim_path(self.service)

    def build(self):
        # remove existing file
        if os.path.exists(self.path):
            os.remove(self.path)

        # list of absolute zim file paths
        zim_files = [os.path.join(self.zim_path, zim) for zim in os.listdir(self.zim_path) if zim.endswith('.zim')]

        if len(zim_files) == 0:
            raise OSError('No ZIM files found in {}, add content'.format(self.zim_path))

        # use kiwix-manage to build new library file
        cmd = '{} {} add {}'.format( tools.kiwix_manage_path(), self.path, ' '.join(zim_files) )
        subprocess.Popen(cmd, shell=True)

    def add(self, zim_path):
        cmd = '{} {} add {}'.format(tools.kiwix_manage_path(), self.path, zim_path)
        subprocess.Popen(cmd, shell=True)


    
