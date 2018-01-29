import urllib
import json

class Nominatim:
    def __init__(self):
        self._json = None

    def query(self, query, endpoint = "https://nominatim.openstreetmap.org/search?format=json&q="):
        response = urllib.urlopen(endpoint + urllib.quote_plus(query, safe=''))
        self._json = json.load(response)

    def areaId(self):
        for d in self._json:
            if 'osm_type' in d and d['osm_type'] == 'relation' and 'osm_id' in d:
                return 3600000000 + int(d['osm_id'])
        return None
