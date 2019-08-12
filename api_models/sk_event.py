import json

from api_models.sk_location import Location
from api_models.sk_performance import Performance
from api_models.sk_venue import Venue

class Event(object):
    # def __init__(self,
    #              display_name: str,
    #              event_type:   str,
    #              # location:     Location or None,
    #              # performances: [Performance] or None,
    #              popularity:   float         or None,
    #              sk_id:        int,
    #              start:        dict,
    #              status:       str,
    #              uri:          str):
    #              # venue:        Venue):

    def __init__(self, event_data: dict):
        # try:
        self.display_name = event_data['displayName']
        self.event_type = event_data['type']
        self.popularity = event_data['popularity']
        self.location = Location(event_data['location'])
        self.performance = [Performance(p_data) for p_data in event_data['performance']]
        self.sk_id = event_data['id']
        self.start = event_data['start']
        self.status = event_data['status']
        self.uri = event_data['uri']
        # self.venue = Venue(event_data['venue'])
        # except Exception as exc:
        #     print(f'Exception {exc} building event')
            # self.display_name = display_name
            # self.event_type   = event_type
            # # self.location     = location
            # # self.performances = performances
            # self.popularity   = popularity
            # self.sk_id        = sk_id
            # self.start        = start
            # self.status       = status
            # self.uri          = uri
            # # self.venue        = venue

    def __str__(self) -> str:
        return self.display_name

        # return f'{", ".join([perf.__str__() for perf in self.performances])}'\
        #        f' @ {self.venue}' if self.venue else '' + f'{self.start}' if self.start else ''


    def __dict__(self):
        return {'display_name': self.display_name,
                'event_type'  : self.event_type,
                'location'    : self.location.__dict__(),
                'performance': [performance.__dict__() for performance in self.performance],
                'popularity'  : self.popularity,
                'sk_id'       : self.sk_id,
                'start'       : self.start,
                'status'      : self.status,
                'uri'         : self.uri}
                # 'venue'       : self.venue.__dict__() if self.venue else None}

    def to_json(self):
        return json.dumps(self, default=lambda e: e.__dict__, sort_keys=True, indent=4)