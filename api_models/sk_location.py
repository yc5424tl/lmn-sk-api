import json

class Location(object):

    def __init__(self, city: dict, lat: float or None = None, lng: float or None = None):
        self.city = city
        self.lat  = lat
        self.lng  = lng

    def __str__(self) -> str:
        return f'CITY: {self.city}  LAT: {self.lat}  LNG: {self.lng}'

    def __dict__(self) -> dict:
        return {'city': self.city,  'lat': self.lat,  'lng': self.lng}

    def to_json(self):
        return json.dumps(self, default=lambda loc: loc.__dict__, sort_keys=True, indent=4)

