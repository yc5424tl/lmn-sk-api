import json

class Performance(object):
    def __init__(self, artist, billing: str, billing_index: int, name: str,sk_id: int):
         self.artist = artist
         self.billing = billing
         self.billing_index = billing_index
         self.name = name
         self.sk_id = sk_id

    def __str__(self):
        return f'ARTIST: {self.name}  SLOT: {self.billing_index} BILL: {self.billing}  SK_ID: {self.sk_id}'

    def __dict__(self):
        return {'artist'       : self.artist.to_dict(),
                'billing'      : self.billing,
                'billing_index': self.billing_index,
                'name'         : self.name,
                'sk_id'        : self.sk_id}

    def to_json(self):
        return json.dumps(self, default=lambda p: p.__dict__, sort_keys=True, indent=4)


