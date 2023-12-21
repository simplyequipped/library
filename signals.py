
class Signals:
    def __init__(self, services):
        self._services = services
        self._signals = {
            'service_url': self._get_service_url,
            'service_is_running': self._get_service_is_running,
            'quit': self._quit
        }

    def _get_service_url(self, data):
        service = data['data']
        if service in self._services:
            return self._services[service].get_url()

    def _get_service_is_running(self, data):
        service = data['data']
        if service in self._services:
            return self._services[service].is_running()

    def _quit(self, data):
        self._services.stop_all()
        return True

    def parse(self, data):
        signal = data['signal']
        if signal in self._signals:
            # call custom signal handling function
            response_data = self._signals[signal](data)
            return {'signal': signal, 'data': response_data}
        
    def __getitem__(self, name):
        return self._signals[name]

    def __setitem__(self, name, service):
        self._signals[name] = service

    def __delitem__(self, name):
        del self._signals[name]

    def __len__(self):
        return len(self._signals)

    def __iter__(self):
        return iter(self._signals)

    def __contains__(self, name):
        return name in self._signals

    def keys(self):
        return list(self._signals.keys())

    def values(self):
        return list(self._signals.values())

    def items(self):
        return list(self._signals.items())
            
