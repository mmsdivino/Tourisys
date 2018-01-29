import googlemaps
import urlparse
import io
import json

class GMapsData:
    _key = 'AIzaSyA0Yst-qoirbQMooKig-qHPRTA2SCMiuFc'
    _gmaps = googlemaps.Client(_key)

    def __init__(self):
        self._review = []
        self._user = []
        self._poi = []

    def _placeId(self, poi):
        placesResult = self._gmaps.places_nearby((poi['latitude'], poi['longitude']), name=poi['name'], rank_by='distance', language='pt-BR')
        for d in placesResult['results']:
            if 'place_id' in d:
                return d['place_id']
        return None

    def _reviews(self, placeId, poi):
        placeDetail = self._gmaps.place(placeId)
        result = placeDetail['result']
        if 'reviews' in result:
            reviews = result['reviews']
            gen = (review for review in reviews if 'author_url' in review)

            i = {}
            i['item_id'] = poi['id']
            i['name'] = poi['name']
            i['category'] = poi['type']
            i['latitude'] = poi['latitude']
            i['longitude'] = poi['longitude']
            self._poi.append(i)

            for review in gen:
                r = {}
                # user_id
                pathUrl = urlparse.urlparse(review['author_url']).path
                r['user_id'] = int(pathUrl.split("/")[3])
                r['item_id'] = poi['id']
                r['rating'] = review['rating']
                self._review.append(r)

                u = {}
                u['user_id'] = r['user_id']
                u['name'] = review['author_name']
                self._user.append(u)

    def data(self, listPoi):
        for poi in listPoi:
            placeId = self._placeId(poi)
            if placeId:
                self._reviews(placeId, poi)

    def json(self):
        with io.open('data/poi.json', 'w', encoding='utf8') as poi_file:
            poi_file.write(unicode(json.dumps(self._poi, ensure_ascii=False)))
        with io.open('data/review.json', 'w', encoding='utf8') as review_file:
            review_file.write(unicode(json.dumps(self._review, ensure_ascii=False)))
        with io.open('data/user.json', 'w', encoding='utf8') as user_file:
            user_file.write(unicode(json.dumps(self._user, ensure_ascii=False)))