import json

from api_models.sk_artist import Artist


class Performance(object):
    # def __init__(self, artist: Artist, billing: str, billing_index: int, name: str,sk_id: int):
    #      self.artist = artist
    #      self.billing = billing
    #      self.billing_index = billing_index
    #      self.name = name
    #      self.sk_id = sk_id

    def __init__(self, perf_data):
        self.artist        = Artist(perf_data['artist'])
        self.billing       = perf_data['billing']
        self.billing_index = perf_data['billingIndex']
        self.name          = perf_data['displayName']
        self.sk_id         = perf_data['id']

    def __str__(self):
        return f'ARTIST: {self.name}  SLOT: {self.billing_index} BILL: {self.billing}  SK_ID: {self.sk_id}'

    def __dict__(self):
        return {'artist'       : self.artist.__dict__(),
                'billing'      : self.billing,
                'billing_index': self.billing_index,
                'name'         : self.name,
                'sk_id'        : self.sk_id}

    def to_json(self):
        return json.dumps(self, default=lambda p: p.__dict__, sort_keys=True, indent=4)


