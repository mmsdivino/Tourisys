import overpy

class OverlayData:
    _categoryLink = [
        {'selector': '["amenity"="arts_centre"]', 'type': 'arts_centre'},
        {'selector': '["tourism"="artwork"][artwork_type!~"statue"]', 'type': 'artwork'},
        {'selector': '["tourism"="attraction"]', 'type': 'attraction'},
        {'selector': '["leisure"="casino"]', 'type': 'casino'},
        {'selector': '["historic"="castle"]', 'type': 'castle'},
        {'selector': '["tourism"="gallery"]', 'type': 'gallery'},
        {'selector': '["heritage"]', 'type': 'heritage'},
        {'selector': '["historic"][historic!~"memorial|monument|statue|castle"]', 'type': 'historic'},
        {'selector': '["tourism"="information"]', 'type': 'information'},
        {'selector': '["historic"~"^monument$|^memorial$"]', 'type': 'monument_memorial'},
        {'selector': '["natural"="tree"]["monument"="yes"]', 'type': 'monumental_tree'},
        {'selector': '["tourism"="museum"]', 'type': 'museum'},
        {'selector': '["tourism"="picnic_site"]', 'type': 'picnic'},
        {'selector': '["leisure"="picnic_table"]', 'type': 'picnic'},
        {'selector': '["historic"="statue"]', 'type': 'statue'},
        {'selector': '["landmark"="statue"]', 'type': 'statue'},
        {'selector': '["tourism"="artwork"]["artwork_type"="statue"]', 'type': 'statue'},
        {'selector': '["tourism"="theme_park"]', 'type': 'theme_park'},
        {'selector': '["tourism"="viewpoint"]', 'type': 'viewpoint'},
        {'selector': '["landuse"="vineyard"]', 'type': 'vineyard'},
        {'selector': '["man_made"="windmill"]', 'type': 'windmill'},
        {'selector': '["man_made"="watermill"]', 'type': 'watermill'},
        {'selector': '["tourism"="zoo"]', 'type': 'zoo'},
    ]

    def __init__(self, timeout = 25):
        self._timeout = timeout
        self.poiList = []

    def _saveInfo(self, elements, category):
        for element in elements or []:
            if not any(d['id'] == element.id for d in self.poiList):
                poi = {}
                if element._type_value == 'node':
                    poi['latitude'] = float(element.lat)
                    poi['longitude'] = float(element.lon)
                else:
                    poi['latitude'] = float(element.center_lat)
                    poi['longitude'] = float(element.center_lon)
                poi['id'] = element.id
                poi['name'] = element.tags['name']
                poi['type'] = [category]
                self.poiList.append(poi)
            else:
                for d in self.poiList:
                    if d['id'] == element.id:
                        d['type'].append(category)

    def poiData(self, areaId):
        api = overpy.Overpass()
        for category in self._categoryLink:
            elements = []
            query = '[timeout:{}][out:json];' \
                        'area({})->.searchArea;' \
                        'node(area.searchArea);' \
                        'node._["name"]{};(._;>;);out center;'.format(self._timeout, areaId, category['selector']);
            result = api.query(query)
            elements.extend(result.nodes)

            query = '[timeout:{}][out:json];' \
                    'area({})->.searchArea;' \
                    'way(area.searchArea);' \
                    'way._["name"]{};(._;>;);out center;'.format(self._timeout, areaId, category['selector']);
            result = api.query(query)
            elements.extend(result.ways)

            query = '[timeout:{}][out:json];' \
                    'area({})->.searchArea;' \
                    'rel(area.searchArea);' \
                    'rel._["name"]{};(._;>;);out center;'.format(self._timeout, areaId, category['selector']);
            result = api.query(query)
            elements.extend(result.relations)
            self._saveInfo(elements, category['type'])