from math import radians, sin, cos, sqrt, atan2

class cluster:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.radius = 0
        self.__listMarker = list()

    def __updateRadius(self, marker):
        #compute radius in meters from coordinates

        R = 6371  # earth radius
        dLat = radians(marker[0] - self.latitude)
        dLon = radians(marker[1] - self.longitude)
        lat1 = radians(self.latitude)
        lat2 = radians(marker[0])

        a = sin(dLat/2) * sin(dLat/2) +\
            sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2)

        c = 2 * atan2(sqrt(a), sqrt(1-a))
        newDist = R * c * 1000

        if newDist > self.radius:
            self.radius = newDist

    def addMarker(self, marker):
        self.__listMarker.append(marker)
        self.__updateRadius(marker)
