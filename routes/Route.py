import io
import webbrowser
import os

class Route:
    def __init__(self, latitudes, longitudes):
        self._latitudes = latitudes
        self._longitudes = longitudes

    def _waypoints(self):
        endpoint = 'var waypoints = [';
        for lat, lng in zip(self._latitudes, self._longitudes):
            endpoint += '{lat: %s, lng: %s}, ' % (lat, lng)
        endpoint = endpoint[:-2]
        endpoint += ']'
        return endpoint

    def map(self):
        with io.open('routes/location.js', 'w', encoding='utf8') as location_file:
            location_file.write(unicode(self._waypoints()))
        webbrowser.open('file://' + os.path.realpath('routes/route_sample.html'))