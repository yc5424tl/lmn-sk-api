import json

class Location(object):
    def __init__(self, city: str, lat: float or None, lng: float or None):
                self.city = city
                self.lat  = lat
                self.lng  = lng

    def __str__(self) -> str:
        return f'CITY: {self.city}'

    def __dict__(self) -> dict:
        return {'city': self.city}

    def to_json(self):
        return json.dumps(self, default=lambda loc: loc.__dict__, sort_keys=True, indent=4)

