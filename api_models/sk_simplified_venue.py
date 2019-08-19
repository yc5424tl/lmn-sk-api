
class SimplifiedVenue:

    def __init__(self, sk_id: int, display_name: str, uri: str, metro_area: dict or None):
        self.sk_id = sk_id
        self.display_name = display_name
        self.uri = uri
        self.metro_area = metro_area

    def __str__(self):
        return f'NAME: {self.display_name}  ID: {self.sk_id}  URI: {self.uri}'

    def __dict__(self):
        return {'name': self.display_name, 'id': self.sk_id, 'uri': self.uri, 'metro_area': self.metro_area}