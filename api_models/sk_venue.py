import json
from api_models.sk_location import Location

class Venue(object):

    def __init__(self,
                 capacity: int or None,
                 location: Location,
                 display_name: str,
                 uri: str,
                 phone_num: str or None,
                 sk_id: int,
                 street: str or None,
                 zip_code: str or None,
                 website: str or None,
                 description: str or None):

        self.capacity = capacity
        self.location = location
        self.display_name = display_name
        self.uri = uri
        self.phone_num = phone_num
        self.sk_id = sk_id
        self.street = street
        self.zip_code = zip_code
        self.website = website
        self.description = description


    def __str__(self):
        return f'{self.display_name} in {self.location.city}'

    def __dict__(self):
        return { 'name': self.display_name, 'city': self.location.city, 'uri': self.uri, 'id': self.sk_id }

    def to_json(self):
        return json.dumps(self, default=lambda v: v.__dict__, sort_keys=True, indent=4)

