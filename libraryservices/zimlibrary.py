import os
import subprocess

# local imports
import libraryservices


class ZimLibrary:
    def __init__(self, service):
        self.service = service
        self.path = libraryservices.kiwix_library_path(self.service)
        self.zim_path = libraryservices.kiwix_zim_path(self.service)

    def build(self):
        # list of absolute zim file paths
        zim_files = [os.path.join(self.zim_path, zim) for zim in os.listdir(self.zim_path) if zim.endswith('.zim')]

        # cannot build library without zim files
        if len(zim_files) == 0:
            return

        # remove existing file
        if os.path.exists(self.path):
            os.remove(self.path)

        # use kiwix-manage to build new library file
        cmd = '{} {} add {}'.format( libraryservices.KIWIX_MANAGE_PATH, self.path, ' '.join(zim_files) )
        subprocess.run(cmd, shell=True)

    def add(self, zim_path):
        cmd = '{} {} add {}'.format(libraryservices.KIWIX_MANAGE_PATH, self.path, zim_path)
        subprocess.run(cmd, shell=True)


    
