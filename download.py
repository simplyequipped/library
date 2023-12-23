import os
import csv
import urllib.request

from concurrent.futures import ThreadPoolExecutor

# local imports
import tools


class DownloadContent:
    # status
    NOT_STARTED = 'not started'
    DOWNLOADING = 'downloading'
    COMPLETE = 'complete'

    def __init__(self, csv_file):
        self.status = DownloadContent.NOT_STARTED
        self.csv_file = csv_file
        self._url_size_data = {}
        self.urls = {}
        self.downloading = []
        self.downloaded = []
        self.failed = []
        self.skipped = []
        self.skip_if_exists = True
        self.max_concurrent_downloads = 3
        self._destination_dir = None
        self._complete_callback = None
        self._downloading_callback = None
        self._progress_callback = None

        self._parse_csv()
        self.total_size = sum( [size for size in self._url_size_data.values()] )

    def set_complete_callback(self, callback):
        self._complete_callback = callback

    def set_downloading_callback(self, callback):
        self._downloading_callback = callback

    def set_progress_callback(self, callback):
        self._progress_callback = callback

    def services(self):
        return self.urls.keys()

    def progress(self):
        complete_urls = self.downloaded + self.skipped + self.failed
        complete_size = sum( [size for url, size in self._size_data if url in complete_urls] )
        # percentage
        return int( (complete_size / self.total_size) * 100 )

    def download(self):
        self.status = DownloadContent.DOWNLOADING

        for service in self.urls:
            # use the service specifc zim path as the destination
            self._destination_dir = tools.kiwix_zim_path(service)
            # download files concurrently
            with ThreadPoolExecutor(max_workers=self.max_concurrent_downloads) as executor:
                executor.map(self._download_file, self.urls[service])

        self.status = DownloadContent.COMPLETE
        if self._complete_callback is not None:
            self._complete_callback(self)

    def _download_file(self, url):
        try:
            file_name = url.split('/')[-1]
            file_path = os.path.join(self._destination_dir, file_name)

            if self.skip_if_exists and os.path.exists(file_path):
                self.skipped.append(url)

                if self._progress_callback is not None:
                    self._progress_callback( self.progress() )

                return

            self.downloading.append(file_name)
            if self._downloading_callback is not None:
                self._downloading_callback( self.downloading )

            # download file
            urllib.request.urlretrieve(url, file_path)
            self.downloaded.append(url)
        except Exception as e:
            self.failed.append(url)

        self.downloading.remove(file_name)

        if self._progress_callback is not None:
            self._progress_callback( self.progress() )

    def _parse_csv(self):
        # get content urls from csv
        with open(self.csv_file, newline='') as f:
            csv_reader = csv.reader(f)
        
            for row in csv_reader:
                # skip blank rows
                if len(row) == 0:
                    continue

                service = row[0].lower()
                
                # skip title row
                if service == 'service':
                    continue
        
                # dynamically group urls based on service
                if service not in self.urls:
                    self.urls[service] = []
        
                url = row[6]
                file_size = float(row[5].split()[0])
                self._url_size_data[url] = file_size
                self.urls[service].append(url)

