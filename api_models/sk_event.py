import json

from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_venue import Venue

class Event(object):
    def __init__(self,
                 display_name: str           or None,
                 event_type:   str           or None,
                 location:     Location      or None,
                 performances: [Performance] or None,
                 popularity:   float         or None,
                 sk_id:        int           or None,
                 start:        dict          or None,
                 status:       str           or None,
                 uri:          str           or None,
                 venue:        Venue         or None ):

        self.display_name = display_name
        self.event_type   = event_type
        self.location     = location
        self.performances = performances
        self.popularity   = popularity
        self.sk_id        = sk_id
        self.start        = start
        self.status       = status
        self.uri          = uri
        self.venue        = venue

    def __str__(self) -> str:
        return f'{", ".join([perf.__str__() for perf in self.performances])}'\
               f' @ {self.venue}' if self.venue else '' + f'{self.start}' if self.start else ''

    def __dict__(self):
        return {'display_name': self.display_name,
                'event_type'  : self.event_type,
                'location'    : self.location.__dict__(),
                'performances': [performance.__dict__() for performance in self.performances],
                'popularity'  : self.popularity,
                'sk_id'       : self.sk_id,
                'start'       : self.start,
                'status'      : self.status,
                'uri'         : self.uri,
                'venue'       : self.venue.__dict__() }

    def to_json(self):
        return json.dumps(self, default=lambda e: e.__dict__, sort_keys=True, indent=4)