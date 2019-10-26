
class Artist(object):

    def __init__(self, display_name: str, uri: str, sk_id: int):
        self.display_name = display_name
        self.sk_id = sk_id
        self.uri = uri

    def __str__(self):
        return f'ID: {self.sk_id} NAME: {self.display_name} URI: {self.uri}'

    def __dict__(self):
        return {'sk_id': self.sk_id, 'display_name': self.display_name, 'uri': self.uri}


