# encoding: utf-8

import urllib, json, googlemaps, urlparse
import sys

reload(sys)
sys.setdefaultencoding('latin-1')

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

    def getPOIData(self, listPoi):
        response = urllib.urlopen(self.url)
        data = json.loads(response.read(), encoding='latin-1')
        elements = data['elements']
        for element in elements:
            if 'tags' in element and 'name' in element['tags']:
                if not any(d['id'] == element['id'] for d in listPoi):
                    poi = {}
                    if element['type'] == 'node':
                        poi['location'] = (element['lat'], element['lon'])
                    else:
                        poi['location'] = (element['center']['lat'], element['center']['lon'])
                    poi['id'] = element['id']
                    poi['name'] = element['tags']['name'].encode('latin-1')
                    poi['type'] = [self.type]
                    listPoi.append(poi)
                else:
                    for d in listPoi:
                        if d['id'] == element['id']:
                            d['type'].append(self.type)


    def getGMapsData(self, listPoi):
        gmaps = googlemaps.Client(self.key)
        for poi in listPoi:
            placesResult = gmaps.places_nearby(poi['location'], name=poi['name'], rank_by='distance', language='pt-BR')
            if len(placesResult['results']) > 0:
                if 'place_id' in placesResult['results'][0]:
                    placeId = placesResult['results'][0]['place_id']
                    placeDetail = gmaps.place(placeId)
                    if 'reviews' in placeDetail['result']:
                        with open("data/poi_data_0.txt", "a") as poiInfo:
                            poiInfo.write("%s;%s;%s;%s\n" % (poi['id'], placesResult['results'][0]['name'], poi['type'], poi['location']))
                        reviews = placeDetail['result']['reviews'];
                        reviewsList = []
                        for review in reviews:
                            if 'author_url' in review:
                                r = []
                                r.append(poi['id'])
                                pathUrl = urlparse.urlparse(review['author_url']).path
                                r.append(pathUrl.split("/")[3])
                                r.append(review['rating'])
                                r.append(review['time'])
                                reviewsList.append(r)
                        with open("data/ratings_0.txt", "a") as ratings:
                            for item in reviewsList:
                                ratings.write("%s\n" % item)





