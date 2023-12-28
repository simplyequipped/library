# Note: all signals* functions must return a value so a 200 code can be sent

class Signals:
    def __init__(self, services):
        self.services = services
        self.signals = {
            'service_url': self._signal_service_url,
            'service_active': self._signal_service_active,
            'download_start': self._signal_download_start,
            'download_pause': self._signal_download_pause,
            'download_resume': self._signal_download_resume,
            'download_stop': self._signal_download_stop,
            'download_progress': self._signal_download_progress,
            'download_downloading': self._signal_download_downloading,
            'download_downloaded': self._signal_download_downloaded,
            'download_skipped': self._signal_download_skipped,
            'download_failed': self._signal_download_failed,
            'download_complete': self._signal_download_complete,
            'quit': self._signal_quit
        }

    def _signal_service_url(self, data):
        service = data['data']
        if service in self.services:
            return self.services[service].url()

    def _signal_service_active(self, data):
        service = data['data']
        if service in self.services:
            return self.services[service].active()

    def _signal_download_start(self, data):
        self.services.content.download()
        return self.services.content.progress()

    def _signal_download_pause(self, data):
        self.services.content.pause()
        return True

    def _signal_download_resume(self, data):
        self.services.content.resume()
        return True

    def _signal_download_stop(self, data):
        self.services.content.stop()
        return True

    def _signal_download_progress(self, data):
        return self.services.content.progress()

    def _signal_download_downloading(self, data):
        urls = self.services.content.downloading
        return [url.split('/')[-1] for url in urls]

    def _signal_download_downloaded(self, data):
        urls = self.services.content.downloaded
        return [url.split('/')[-1] for url in urls]

    def _signal_download_skipped(self, data):
        urls = self.services.content.skipped
        return [url.split('/')[-1] for url in urls]

    def _signal_download_failed(self, data):
        urls = self.services.content.failed
        return [url.split('/')[-1] for url in urls]

    def _signal_download_complete(self, data):
        complete = self.services.content.complete()

        # restart services if download complete
        if complete:
            self.services.rebuild_zim()

        return complete

    def _signal_quit(self, data):
        self.services.stop_except_http()
        return True

    def parse(self, data):
        signal = data['signal']
        if signal in self.signals:
            # call custom signal handling function
            response_data = self.signals[signal](data)
            return {'signal': signal, 'data': response_data}
        
    def __getitem__(self, name):
        return self.signals[name]

    def __setitem__(self, name, service):
        self.signals[name] = service

    def __delitem__(self, name):
        del self.signals[name]

    def __len__(self):
        return len(self.signals)

    def __iter__(self):
        return iter(self.signals)

    def __contains__(self, name):
        return name in self.signals

    def keys(self):
        return list(self.signals.keys())

    def values(self):
        return list(self.signals.values())

    def items(self):
        return list(self.signals.items())
            
