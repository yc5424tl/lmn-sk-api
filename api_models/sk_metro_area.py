import json

class MetroArea(object):

    def __init__(self, sk_id: int or None, uri: str or None, display_name: str or None, country: dict or None):
         self.sk_id        = sk_id
         self.uri          = uri
         self.display_name = display_name
         self.country      = country

    def __str__(self):
        return f'ID: {self.sk_id} URI: {self.uri} NAME: {self.display_name} COUNTRY: {self.country.displayName}'

    def __dict__(self):
        return {'sk_id': self.sk_id, 'uri': self.uri, 'display_name': self.display_name,'country': self.country }

    def to_json(self):
        return json.dumps(self, default=lambda m: m.__dict__, sort_keys=True, indent=4)
