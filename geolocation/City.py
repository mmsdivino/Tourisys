import urllib.request, json

class City:
    def __init__(self, url):
        self.url = url
        self.getBoundingBox()

    def getBoundingBox(self):
        with urllib.request.urlopen(self.url) as url:
            data = json.loads(url.read().decode())
            self.west = data[0]['boundingbox'][0]
            self.east = data[0]['boundingbox'][1]
            self.south = data[0]['boundingbox'][2]
            self.north = data[0]['boundingbox'][3]

    def __str__(self):
        return self.south + "," + self.west + "," + self.north + "," + self.east
