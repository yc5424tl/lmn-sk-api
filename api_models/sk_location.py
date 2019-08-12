import json

class Location(object):

    # def __init__(self, city: dict, lat: float or None = None, lng: float or None = None):
    #     self.city = city
    #     self.lat  = lat
    #     self.lng  = lng

    def __init__(self, location_data: dict):
        self.city = location_data['city']
        # self.lat  = location_data['lat'] if location_data['lat'] else None
        # self.lng  = location_data['lng'] if location_data['lng'] else None

    def __str__(self) -> str:
        return f'CITY: {self.city}'

               # f' LAT: {self.lat}  LNG: {self.lng}'

    def __dict__(self) -> dict:
        return {'city': self.city}

    def to_json(self):
        return json.dumps(self, default=lambda loc: loc.__dict__, sort_keys=True, indent=4)

