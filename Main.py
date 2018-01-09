from geolocation.City import *
from poi.OverlayData import *

salvador = City("http://nominatim.openstreetmap.org/search/brazil/bahia/salvador?format=json")
artsCentre = OverlayData("[amenity=arts_centre]", salvador.__str__(), "arts_centre")
artwork = OverlayData("[tourism=artwork][artwork_type!~%27statue%27]", salvador.__str__(), "artwork")
attraction = OverlayData("[tourism=attraction]", salvador.__str__(), "attraction")
castle = OverlayData("[historic=castle]", salvador.__str__(), "castle")
gallery = OverlayData("[tourism=gallery]", salvador.__str__(), "gallery")
heritage = OverlayData("[heritage]", salvador.__str__(), "heritage")
historic = OverlayData("[historic][historic!~%27memorial|monument|statue|castle%27]", salvador.__str__(), "historic")
information = OverlayData("[tourism=information]", salvador.__str__(), "information")
monument_memorial = OverlayData("[historic~%27^monument$|^memorial$%27]", salvador.__str__(), "monument_memorial")
museum = OverlayData("[tourism=museum]", salvador.__str__(), "museum")
viewpoint = OverlayData("[tourism=viewpoint]", salvador.__str__(), "viewpoint")
zoo = OverlayData("[tourism=zoo]", salvador.__str__(), "zoo")