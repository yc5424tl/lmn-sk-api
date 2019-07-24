import json
from api_models.sk_metro_area import MetroArea

class Venue(object):
    def __init__(self,
                 capacity   : int or None,
                 city       : dict, # City Class
                 description: str or None,
                 lat        : float or None,
                 lng        : float or None,
                 metro_area : MetroArea or None,
                 name       : str,
                 phone      : str or None,
                 sk_id      : int,
                 street     : str or None,
                 uri        : str,
                 website    : str or None,
                 zip_code   : str or None):

                self.capacity    = capacity
                self.city        = city
                self.description = description
                self.lat         = lat
                self.lng         = lng
                self.metro_area  = metro_area
                self.name        = name
                self.phone       = phone
                self.sk_id       = sk_id
                self.street      = street
                self.uri         = uri
                self.website     = website
                self.zip_code    = zip_code

    def __str__(self):
        return f'{self.name} @ {self.street} in {self.city} {self.website} {self.phone}'

    def __dict__(self):
        return {'capacity'   : self.capacity,
                'city'       : self.city,
                'description': self.description,
                'lat'        : self.lat,
                'lng'        : self.lng,
                'metro_area' : self.metro_area.__dict__(),
                'name'       : self.name,
                'phone'      : self.phone,
                'sk_id'      : self.sk_id,
                'street'     : self.street,
                'uri'        : self.uri,
                'website'    : self.website,
                'zip_code'   : self.zip_code }

    def to_json(self):
        return json.dumps(self, default=lambda v: v.__dict__, sort_keys=True, indent=4)

