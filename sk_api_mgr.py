import json
import os
from logging import Logger

from api_models.sk_artist import Artist
from api_models.sk_event import Event
from api_models.sk_venue import Venue
from sk_query_mgr import Query


from sk_factory import Factory
import sk_factory
import pprint
pp = pprint.PrettyPrinter()

search_ip_endpoint = "http://api.songkick.com/api/3.0/events.json?apikey={}&location=ip:{}"
log = Logger
Query = Query()
event_count = 0




class API:
    def __init__(self):
        self.key = os.getenv('SK_API_KEY')
        self.factory = Factory()



    def search_for_artist(self, artist_name: str, match_first: bool) -> [Artist] or False:
        response_dict = Query.search_artists_by_name(artist_name, match_first=match_first)
        try:
            if match_first:
                new_artist = self.factory.build_artist(response_dict)
                return [new_artist]
            else:
                matching_artists_list = []
                for artist in response_dict:
                    new_artist = self.factory.build_artist(artist)
                    matching_artists_list.append(new_artist)
                return matching_artists_list
        except TypeError:
            return False


    def search_venues(self, venue_name: str, first_match: bool) -> [Venue]:
        response = Query.search_venues_by_name(venue_name, first_match=first_match)
        try:
            if first_match:
                venue_list = self.instantiate_venues_from_list(response)
                return venue_list
            else:
                venue_list = self.instantiate_venues_from_list(response)
                return venue_list
        except TypeError:
            return False




    def search_artist_id_for_upcoming_events(self, artist_id: int) -> [Event] or []:
        event_dict_list = Query.search_artist_upcoming_events(artist_id)
        if len(event_dict_list) == 0:
            return []
        else:
            events_list = self.instantiate_events_from_list(event_dict_list)
            return events_list

    def search_events_by_metro_area(self, metro_area_id: int) -> [Event] or []:
        event_dict_list = Query.search_events_by_metro_area(metro_area_id)
        if not event_dict_list:
            return []
        else:
            event_list = self.instantiate_events_from_list(event_dict_list)
            return event_list

    def search_artist_gigography(self, artist_id: int):
        event_dict_list = Query.gigography(artist_id)
        if not event_dict_list:
            return []
        else:
            event_list = self.instantiate_events_from_list(event_dict_list)
            return event_list


    def search_venue_id(self, venue_id: int) -> [Venue] or []:
        venue_dict = Query.search_venue_by_id(venue_id)
        if not venue_dict:
            return []
        else:
            venue_list = self.instantiate_venues_from_list([venue_dict])
            return venue_list


    def search_venue_id_for_upcoming_events(self, venue_id: int) -> [Event]:
        event_dict_list = Query.search_venue_upcoming_events(venue_id)
        if not event_dict_list:
            return []
        else:
            events_list = self.instantiate_events_from_list(event_dict_list)
            return events_list




    def instantiate_events_from_list(self, event_list: [{}]) -> [Event] or []:
        if not event_list:
            return []
        else:
            events = []
            for event in event_list:
                try:
                    new_event = self.factory.build_event(event)
                    events.append(new_event)
                except KeyError as kE:
                    log(f'Key not present in event(dict): {str(kE)}')
            return events



    def instantiate_venues_from_list(self, venue_list: [{}]) -> [Venue]:
        if len(venue_list) == 0:
            return []
        else:
            venues_list = []
            for venue in venue_list:
                new_venue = self.factory.build_venue(venue)
                venues_list.append(new_venue)
            return venues_list


    def instantiate_artists_from_list(self, artist_list: [{}]) -> [Artist]:
        if not artist_list:
            return []
        else:
            artists_list = []
            for artist in artist_list:
                try:
                    new_artist = self.factory.build_artist(artist)
                    artists_list.append(new_artist)
                except KeyError as kE:
                    log(f'KeyError {kE} during instantiating artists from list passing {artist}')
            return artists_list


    @staticmethod
    def instantiate_list_data(list_data:[{}], call: str):
        if not bool(len(list_data)):
            return []
        else:
            instance_list = []
            for data in list_data:
                try:
                    # new_instance = self.factory.build_event(data)
                    new_instance = sk_factory.instance_call(list_data=data, call=call)
                    instance_list.append(new_instance)
                except KeyError as kE:
                    log(f'KeyError {kE} during {call} instance call passing {data}')
            return instance_list

    @staticmethod
    def serialize_list(dict_list: [{}]):
        serial_list = []
        for obj in dict_list:
            serial_list.append(json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o))))
        return serial_list


