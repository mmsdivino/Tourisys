from geolocation.City import *
from poi.OverlayData import *

salvador = City("http://nominatim.openstreetmap.org/search/brazil/bahia/salvador?format=json")

processedElements = []

artsCentre = OverlayData("[amenity=arts_centre]", salvador.__str__(), "arts_centre")
artsCentre.getPOIData(processedElements)
artwork = OverlayData("[tourism=artwork][artwork_type!~%27statue%27]", salvador.__str__(), "artwork")
artwork.getPOIData(processedElements)
attraction = OverlayData("[tourism=attraction]", salvador.__str__(), "attraction")
attraction.getPOIData(processedElements)
castle = OverlayData("[historic=castle]", salvador.__str__(), "castle")
castle.getPOIData(processedElements)
gallery = OverlayData("[tourism=gallery]", salvador.__str__(), "gallery")
gallery.getPOIData(processedElements)
heritage = OverlayData("[heritage]", salvador.__str__(), "heritage")
heritage.getPOIData(processedElements)
historic = OverlayData("[historic][historic!~%27memorial|monument|statue|castle%27]", salvador.__str__(), "historic")
historic.getPOIData(processedElements)
information = OverlayData("[tourism=information]", salvador.__str__(), "information")
information.getPOIData(processedElements)
monument_memorial = OverlayData("[historic~%27^monument$|^memorial$%27]", salvador.__str__(), "monument_memorial")
monument_memorial.getPOIData(processedElements)
museum = OverlayData("[tourism=museum]", salvador.__str__(), "museum")
museum.getPOIData(processedElements)
viewpoint = OverlayData("[tourism=viewpoint]", salvador.__str__(), "viewpoint")
viewpoint.getPOIData(processedElements)
zoo = OverlayData("[tourism=zoo]", salvador.__str__(), "zoo")
zoo.getPOIData(processedElements)

zoo.getGMapsData(processedElements)

# print(processedElements)