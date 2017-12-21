import urllib.request, json, googlemaps, urllib.parse

class OverlayData:
    domain = 'http://overpass-api.de/api/interpreter/?data=[out:json];'
    sufix = ';(._;%3E;);out;&bbox='
    gMapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    key = 'AIzaSyA8stzbZM7IgnAVDXPNTQZT6rmW_FzZUFg'

    def __init__(self, parameter, city, type):
        self.parameter = parameter
        self.city = city
        self.type = type
        self.url = \
            self.domain + \
            '(node' + self.parameter + \
            "(bbox))" + \
            self.sufix + self.city
        self.getPOIData()

    def getPOIData(self):
        with urllib.request.urlopen(self.url) as url:
            data = json.loads(url.read().decode())
            elements = data['elements']
            for element in elements:
                poi = {}
                poi['location'] = (element['lat'], element['lon'])
                if 'name' not in element['tags']:
                    poi['name'] = self.type
                else:
                    poi['name'] = element['tags']['name']
                self.getGMapsData(poi)

    def getGMapsData(self, poi):
        gmaps = googlemaps.Client(self.key)
        placesResult = gmaps.places(poi['name'], location=poi['location'], radius=1)
        if len(placesResult['results']) > 0:
            if 'place_id' in placesResult['results'][0]:
                placeId = placesResult['results'][0]['place_id']
                placeDetail = gmaps.place(placeId)
                if 'reviews' in placeDetail['result']:
                    reviews = placeDetail['result']['reviews'];
                    reviewsList = []
                    for review in reviews:
                        r = []
                        r.append(placeId)
                        if 'author_url' in review:
                            pathUrl = urllib.parse.urlsplit(review['author_url']).path
                            r.append(pathUrl.split("/")[3])
                        r.append(review['rating'])
                        r.append(review['time'])
                        reviewsList.append(r)
                    with open("data/ratings_0.txt", "a") as ratings:
                        for item in reviewsList:
                            ratings.write("%s\n" % item)




