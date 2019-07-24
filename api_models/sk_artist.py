from datetime import date


class Artist(object):
    def __init__(self, sk_id: int, display_name: str, uri: str, tour_end_date: date or None):
        self.sk_id = sk_id
        self.display_name = display_name
        self.uri = uri
        self.tour_end_date = tour_end_date

    def __str__(self):
        return f'ID: {self.sk_id} NAME: {self.display_name} URI: {self.uri} END OF TOUR: {self.tour_end_date}'

    def to_dict(self):
        return {'sk_id': self.sk_id, 'display_name': self.display_name, 'uri': self.uri, 'tour_end_date': self.tour_end_date}

