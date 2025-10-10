class GeocodingResult:
    def __init__(self, address, latitude, longitude):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude
        }