import json

class City(object):
    def __init__(self, sk_id: int or None, display_name: str or None, uri: str or None, country: dict or None):
        self.sk_id   = sk_id
        self.display_name    = display_name
        self.uri     = uri
        self.country = country

    def __str__(self) -> str:
        return f'ID: {self.sk_id} NAME: {self.display_name} URI: {self.uri} COUNTRY: {self.country["displayName"]}'

    def to_json(self):
        return json.dumps(self, default=lambda c: c.__dict__, sort_keys=True, indent=4)