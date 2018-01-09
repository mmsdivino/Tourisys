import urllib, json, googlemaps, unicodedata, urlparse

class OverlayData:
    domain = 'http://overpass-api.de/api/interpreter/?data=[out:json];'
    sufix = ';(._;%3E;);out%20center;&bbox='
    gMapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    key = 'AIzaSyA0Yst-qoirbQMooKig-qHPRTA2SCMiuFc'

    def __init__(self, parameter, city, type):
        self.parameter = parameter
        self.city = city
        self.type = type
        self.url = \
            self.domain + \
            '(node' + self.parameter + \
            "(bbox);way" + self.parameter + \
            "(bbox);rel" + self.parameter + \
            "(bbox))" + self.sufix + self.city
        self.getPOIData()

    def getPOIData(self):
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        elements = data['elements']
        for element in elements:
            if 'tags' in element:
                if 'name' in element['tags']:
                    poi = {}
                    if element['type'] == 'node':
                        poi['location'] = (element['lat'], element['lon'])
                    else:
                        poi['location'] = (element['center']['lat'], element['center']['lon'])
                    poi['name'] = unicodedata.normalize('NFKD', element['tags']['name']).encode('ascii','ignore')
                    poi['type'] = self.type
                    self.getGMapsData(poi)

    def getGMapsData(self, poi):
        gmaps = googlemaps.Client(self.key)
        placesResult = gmaps.places_nearby(poi['location'], name=poi['name'], rank_by='distance')
        if len(placesResult['results']) > 0:
            if 'place_id' in placesResult['results'][0]:
                placeId = placesResult['results'][0]['place_id']
                placeDetail = gmaps.place(placeId)
                if 'reviews' in placeDetail['result']:
                    with open("data/poi_data_0.txt", "a") as poiInfo:
                        poiInfo.write("%s;%s;%s\n" % (placeId, unicodedata.normalize('NFKD', placesResult['results'][0]['name']).encode('ascii','ignore'), poi['type']))
                    reviews = placeDetail['result']['reviews'];
                    reviewsList = []
                    for review in reviews:
                        if 'author_url' in review:
                            r = []
                            r.append(placeId)
                            pathUrl = urlparse.urlparse(review['author_url']).path
                            r.append(pathUrl.split("/")[3])
                            r.append(review['rating'])
                            r.append(review['time'])
                            reviewsList.append(r)
                    with open("data/ratings_0.txt", "a") as ratings:
                        for item in reviewsList:
                            ratings.write("%s\n" % item)





