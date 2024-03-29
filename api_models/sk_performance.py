import json
from api_models.sk_artist import Artist

class Performance(object):

    def __init__(self, artist: Artist, billing: str, billing_index: int, display_name: str, sk_id: int):
        self.artist        = artist
        self.billing       = billing
        self.billing_index = billing_index
        self.display_name  = display_name
        self.sk_id         = sk_id

    def __str__(self):
        return f'ARTIST: {self.display_name}  SLOT: {self.billing_index} BILL: {self.billing}  SK_ID: {self.sk_id}'

    def __dict__(self):
        return {'artist': self.artist.__dict__(),
                'billing': self.billing,
                'billing_index': self.billing_index,
                'display_name': self.display_name,
                'sk_id': self.sk_id}

    def to_json(self):
        return json.dumps(self, default=lambda p: p.__dict__, sort_keys=True, indent=4)


